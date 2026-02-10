from sqlalchemy.orm import Session
from app.models.policy import Policy
from app.models.to_csv import RegisterUser
from app.services.policy_calc_service import compute_policy


async def create_policy_draft(
    draft: RegisterUser,
    employee_tab_number: str,
    arrived_for_hire: bool,
    lang: str | None,
    policy_variant: str | None,
    db: Session,
) -> int:
    """
    1) сохраняем RAW
    2) сразу считаем computed и записываем (но статус пока PENDING_PAYMENT)
    """
    policy = Policy(
        status="PENDING_PAYMENT",
        employee_tab_number=employee_tab_number,
        arrived_for_hire=arrived_for_hire,

        first_name=draft.user.first_name,
        last_name=draft.user.last_name,
        middle_name=draft.user.middle_name,
        birthday=draft.user.birthday,
        passport_series=draft.user.passport_series,
        passport_number=draft.user.passport_number,

        contacts_email=draft.contacts.email,
        contacts_phone_number=draft.contacts.phone_number,

        lang=lang,
        policy_variant=policy_variant,

        policy_title=draft.policy.title,
        price=float(draft.policy.amount),
    )
    db.add(policy)
    db.commit()
    db.refresh(policy)

    # ✅ считаем computed сразу после получения policy.id
    computed = compute_policy(
        employee_tab_number=policy.employee_tab_number,
        arrived_for_hire=policy.arrived_for_hire,
        last_name=policy.last_name,
        first_name=policy.first_name,
        middle_name=policy.middle_name,
        birthday=policy.birthday,
        passport_series=policy.passport_series,
        passport_number=policy.passport_number,
        seq=policy.id,  # используем id записи вместо "строка в excel"
    )

    policy.policy_number = computed.policy_number
    policy.issue_date = computed.issue_date
    policy.arrival_purpose = computed.arrival_purpose
    policy.start_date = computed.start_date
    policy.end_date = computed.end_date
    policy.insurance_days = computed.insurance_days
    policy.premium_total = computed.premium_total

    db.commit()
    db.refresh(policy)

    return policy.id


async def mark_policy_paid(policy_id: int, tx_id: str, db: Session) -> bool:
    policy = db.query(Policy).filter(Policy.id == policy_id).first()
    if not policy:
        return False
    policy.status = "PAID"
    policy.tx_id = tx_id
    db.commit()
    return True


async def get_policy_for_xlsx(policy_id: int, db: Session) -> dict | None:
    policy = db.query(Policy).filter(Policy.id == policy_id).first()
    if not policy or policy.status != "PAID":
        return None

    return {
        "policy_number": policy.policy_number,
        "issue_date": policy.issue_date,
        "start_date": policy.start_date,
        "end_date": policy.end_date,
        "insurance_days": policy.insurance_days,
        "insured_full_name": f"{policy.last_name} {policy.first_name} {policy.middle_name or ''}".strip(),
        "birthday": policy.birthday,
        "document_number": f"{policy.passport_series} {policy.passport_number}".strip(),
        "premium_total": policy.premium_total,
    }

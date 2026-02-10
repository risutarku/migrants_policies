from __future__ import annotations

from datetime import datetime, date
from sqlalchemy import String, Integer, DateTime, Date, Float, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base


class Policy(Base):
    __tablename__ = "policies"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    # статусы: PENDING_PAYMENT -> PAID -> ISSUED
    status: Mapped[str] = mapped_column(String(32), default="PENDING_PAYMENT", index=True)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    # --- RAW данные (то, что ввели/отсканировали) ---
    employee_tab_number: Mapped[str] = mapped_column(String(64))
    arrived_for_hire: Mapped[bool] = mapped_column(Boolean, default=False)

    first_name: Mapped[str] = mapped_column(String(128))
    last_name: Mapped[str] = mapped_column(String(128))
    middle_name: Mapped[str | None] = mapped_column(String(128), nullable=True)

    birthday: Mapped[date] = mapped_column(Date)

    passport_series: Mapped[str] = mapped_column(String(16))
    passport_number: Mapped[str] = mapped_column(String(32))

    contacts_email: Mapped[str | None] = mapped_column(String(256), nullable=True)
    contacts_phone_number: Mapped[str | None] = mapped_column(String(64), nullable=True)

    # UI / бизнес-поля
    lang: Mapped[str | None] = mapped_column(String(16), nullable=True)
    policy_variant: Mapped[str | None] = mapped_column(String(32), nullable=True)  # 'basic' | 'extended'

    policy_title: Mapped[str] = mapped_column(String(128))
    price: Mapped[float] = mapped_column(Float)  # фиксированная цена покупки

    # --- поля после оплаты/выпуска (вычисленные) ---
    policy_number: Mapped[str | None] = mapped_column(String(64), nullable=True, unique=True, index=True)
    issue_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    start_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    end_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    insurance_days: Mapped[int | None] = mapped_column(Integer, nullable=True)

    arrival_purpose: Mapped[str | None] = mapped_column(String(16), nullable=True)  # "РАБОТА"/"СЕМЬЯ"
    reward_amount: Mapped[float | None] = mapped_column(Float, nullable=True)       # зависит от клиента
    premium_total: Mapped[float | None] = mapped_column(Float, nullable=True)       # итоговая премия (расчёт)

    xlsx_path: Mapped[str | None] = mapped_column(String(512), nullable=True)
    tx_id: Mapped[str | None] = mapped_column(String(128), nullable=True)  # если нужно сохранять транзакцию

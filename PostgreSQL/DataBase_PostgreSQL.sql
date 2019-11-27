CREATE TYPE staff_role as ENUM ('doctor', 'nurse', 'receptionist', 'seller', 'primary doctor', 'staff');
CREATE TYPE day_of_week as ENUM ('monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday');
CREATE TYPE gender as ENUM ('male', 'female', 'other');
CREATE TYPE time_slot as ENUM ('0:00','1:00', '2:00', '3:00', '4:00', '5:00', '6:00', '7:00', '8:00', '9:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00', '18:00','19:00','20:00','21:00','22:00','23:00');

CREATE TABLE WeekDay
(
    name day_of_week NOT NULL PRIMARY KEY
);

CREATE TABLE Equipment
(
    id       SERIAL PRIMARY KEY NOT NULL,
    name     VARCHAR(30),
    quantity INTEGER DEFAULT 0
);

CREATE TABLE Staff
(
    ssn         INTEGER PRIMARY KEY NOT NULL,

    role_id     staff_role          NOT NULL,

    office      INTEGER             NOT NULL,
    hiring_date DATE                NOT NULL,
    salary      INTEGER             NOT NULL,
    password    VARCHAR(15)         NOT NULL,

    first_name        VARCHAR(30)         NOT NULL,
    last_name        VARCHAR(30)         NOT NULL,
    birthday    DATE                NOT NULL
);

CREATE TABLE Patient
(
    medical_insurance_id INTEGER PRIMARY KEY,

    name                 VARCHAR(30) NOT NULL,
    birthday             DATE        NOT NULL,
    gender               gender      NOT NULL,
    address              VARCHAR(30) NOT NULL,
    password             VARCHAR(30) NOT NULL
);

CREATE TABLE MedicalHistoryItem
(
    id               SERIAL PRIMARY KEY,

    start_of_illness DATE         NOT NULL,
    end_of_illness   DATE,

    symptoms         TEXT         NOT NULL,
    diagnosis        VARCHAR(255) NOT NULL,

    extra_info       TEXT         NOT NULL,

    patient_id       INTEGER      NOT NULL,

    foreign key (patient_id) references Patient (medical_insurance_id)
);

CREATE TABLE Report
(
    id                      SERIAL PRIMARY KEY,

    content                 TEXT    NOT NULL,

    patient_id              INTEGER NOT NULL,
    medical_history_item_id INTEGER,

    foreign key (patient_id) references Patient (medical_insurance_id),
    foreign key (medical_history_item_id) references MedicalHistoryItem (id)

);

CREATE TABLE Message
(
    id          SERIAL PRIMARY KEY,

    datetime    TIMESTAMP    NOT NULL DEFAULT now(),

    receiver_id INTEGER      NOT NULL,
    sender_id   INTEGER      NOT NULL,
    content     VARCHAR(255) NOT NULL,

    foreign key (receiver_id) references Staff (ssn),
    foreign key (sender_id) references Staff (ssn)
);

CREATE TABLE Bill
(
    id          SERIAL PRIMARY KEY,

    issued_date DATE    NOT NULL DEFAULT now(),

    seller_id   INTEGER NOT NULL,

    patient_id  INTEGER NOT NULL,

    foreign key (seller_id) references Staff (ssn),
    foreign key (patient_id) references Patient (medical_insurance_id)
);

CREATE TABLE Drug
(
    id                SERIAL PRIMARY KEY,

    quantity_in_stock INTEGER            NOT NULL DEFAULT 0,
    expire_date       DATE               NOT NULL,

    name              VARCHAR(50) UNIQUE NOT NULL,

    cost              INTEGER            NOT NULL
);

CREATE TABLE Receipt
(
    id                SERIAL PRIMARY KEY,
    is_used           BOOLEAN DEFAULT FALSE,

    validity_end_date DATE    NOT NULL,

    patient_id        INTEGER NOT NULL,
    doctor_id         INTEGER NOT NULL,

    foreign key (patient_id) references Patient (medical_insurance_id),
    foreign key (doctor_id) references Staff (ssn)
);

CREATE TABLE Appointment
(
    patient_id INTEGER   NOT NULL,
    doctor_id  INTEGER   NOT NULL,

    date DATE NOT NULL,
    slot time_slot NOT NULL,

    primary key (doctor_id, date, slot),

    foreign key (patient_id) references Patient (medical_insurance_id),
    foreign key (doctor_id) references Staff (ssn)
);

CREATE TABLE Notification
(
    patient_id      INTEGER   NOT NULL,
    receptionist_id INTEGER   NOT NULL,

    datetime        TIMESTAMP NOT NULL,
    content         TEXT      NOT NULL,

    primary key (patient_id, datetime),

    foreign key (patient_id) references Patient (medical_insurance_id),
    foreign key (receptionist_id) references Staff (ssn)
);

-- JOIN TABLES

CREATE TABLE WorkDayStaff
(
    day_name  day_of_week NOT NULL,
    staff_ssn INTEGER     NOT NULL,

    foreign key (day_name) references WeekDay (name),
    foreign key (staff_ssn) references Staff (ssn),

    PRIMARY KEY (day_name, staff_ssn)
);

CREATE TABLE EquipmentUsedByStaff
(
    equipment_id INTEGER NOT NULL,
    staff_ssn    INTEGER NOT NULL,

    quantity     INTEGER DEFAULT 1,

    foreign key (equipment_id) references Equipment (id),
    foreign key (staff_ssn) references Staff (ssn),

    PRIMARY KEY (equipment_id, staff_ssn)
);

CREATE TABLE BillContainsDrugs
(
    bill_id  INTEGER NOT NULL,
    drug_id  INTEGER NOT NULL,

    quantity INTEGER NOT NULL,

    primary key (bill_id, drug_id),

    foreign key (bill_id) references Bill (id),
    foreign key (drug_id) references Drug (id)
);

CREATE TABLE ReceiptContainsDrugs
(
    receipt_id INTEGER NOT NULL,
    drug_id    INTEGER NOT NULL,

    quantity   INTEGER NOT NULL,

    primary key (receipt_id, drug_id),

    foreign key (receipt_id) references Receipt (id),
    foreign key (drug_id) references Drug (id)
);

-- VIEWS ---

CREATE VIEW doctors as
SELECT *
from Staff
where Staff.role_id = 'doctor';
CREATE VIEW receptionists as
SELECT *
from Staff
where Staff.role_id = 'receptionist';
CREATE VIEW sellers as
SELECT *
from Staff
where Staff.role_id = 'seller';
CREATE VIEW primary_doctors as
SELECT *
from Staff
where Staff.role_id = 'primary doctor';
CREATE VIEW workers as
SELECT *
from Staff
where Staff.role_id = 'staff';
CREATE VIEW nurses as
SELECT *
from Staff
where Staff.role_id = 'nurse';

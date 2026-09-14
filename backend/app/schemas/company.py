from __future__ import annotations
from datetime import date
from pydantic import BaseModel, ConfigDict

class BrregOrganisasjonsform(BaseModel):
    kode: str
    beskrivelse: str

class BrregAdresse(BaseModel):
    land: str | None = None
    landkode: str | None = None
    postnummer: str | None = None
    poststed: str | None = None
    adresse: list[str] | None = None
    kommune: str | None = None
    kommunenummer: str | None = None

class BrregNaeringskode(BaseModel):
    kode: str
    beskrivelse: str | None = None

class BrregEnhetResponse(BaseModel):
    """Raw response from BRREG Enhetsregisteret API."""
    organisasjonsnummer: str
    navn: str
    organisasjonsform: BrregOrganisasjonsform | None = None
    registreringsdatoEnhetsregisteret: str | None = None
    stiftelsesdato: str | None = None
    slettedato: str | None = None
    forretningsadresse: BrregAdresse | None = None
    postadresse: BrregAdresse | None = None
    naeringskode1: BrregNaeringskode | None = None
    naeringskode2: BrregNaeringskode | None = None
    naeringskode3: BrregNaeringskode | None = None
    antallAnsatte: int | None = None
    harRegistrertAntallAnsatte: bool | None = None
    registrertIMvaregisteret: bool | None = None
    registrertIForetaksregisteret: bool | None = None
    registrertIStiftelsesregisteret: bool | None = None
    registrertIFrivillighetsregisteret: bool | None = None
    sisteInnsendteAarsregnskap: str | None = None
    konkurs: bool | None = None
    underAvvikling: bool | None = None
    underTvangsavviklingEllerTvangsopplosning: bool | None = None
    institusjonellSektorkode: dict | None = None
    maalform: str | None = None
    hjemmeside: str | None = None
    overordnetEnhet: str | None = None  # For underenheter

class CompanyCreate(BaseModel):
    organization_number: str
    name: str

class CompanyRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    organization_number: str
    name: str

class CompanyBrief(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    org_number: str
    name: str
    org_form_code: str | None = None

class CompanyAddressRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    address_type: str
    street_lines: list[str]
    postal_code: str | None = None
    city: str | None = None
    municipality_name: str | None = None
    country: str | None = None

class CompanyRoleRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    role_type_code: str
    role_type_description: str
    person_first_name: str | None = None
    person_last_name: str | None = None
    person_birth_date: str | None = None
    is_resigned: bool = False
    entity_name: str | None = None

class CompanyIndustryRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    priority: int
    nace_code: str
    nace_description: str | None = None

class CompanyAliasRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    alias: str

class CompanyEventRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    event_date: date
    event_type: str
    description: str | None = None

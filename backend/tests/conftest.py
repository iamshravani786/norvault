import pytest
import asyncio
from unittest.mock import AsyncMock, MagicMock

@pytest.fixture
def sample_brreg_enheter_response():
    """Real-format BRREG Enhetsregisteret response."""
    return {
        'organisasjonsnummer': '923609016',
        'navn': 'EQUINOR ASA',
        'organisasjonsform': {'kode': 'ASA', 'beskrivelse': 'Allment aksjeselskap'},
        'registreringsdatoEnhetsregisteret': '2007-11-30',
        'stiftelsesdato': '1972-09-18',
        'forretningsadresse': {
            'land': 'Norge',
            'landkode': 'NO',
            'postnummer': '4035',
            'poststed': 'STAVANGER',
            'adresse': ['Forusbeen 50'],
            'kommune': 'STAVANGER',
            'kommunenummer': '1103'
        },
        'naeringskode1': {'kode': '06.100', 'beskrivelse': 'Utvinning av råolje'},
        'antallAnsatte': 21000,
        'registrertIMvaregisteret': True,
        'registrertIForetaksregisteret': True,
        'sisteInnsendteAarsregnskap': '2024',
        'konkurs': False,
        'underAvvikling': False,
        'underTvangsavviklingEllerTvangsopplosning': False,
        'hjemmeside': 'www.equinor.com',
    }

@pytest.fixture
def sample_brreg_roller_response():
    """Real-format BRREG Roller response."""
    return {
        'rollegrupper': [
            {
                'type': {'kode': 'STYR', 'beskrivelse': 'Styre'},
                'sistEndret': '2024-05-12',
                'roller': [
                    {
                        'type': {'kode': 'LEDE', 'beskrivelse': 'Styreleder'},
                        'person': {
                            'fodselsdato': '1965-03-15',
                            'navn': {'fornavn': 'Jon Erik', 'etternavn': 'Reinhardsen'},
                            'erDoed': False
                        },
                        'fratradt': False,
                    }
                ]
            },
            {
                'type': {'kode': 'DAGL', 'beskrivelse': 'Daglig leder'},
                'roller': [
                    {
                        'type': {'kode': 'DAGL', 'beskrivelse': 'Daglig leder/ adm.direktør'},
                        'person': {
                            'fodselsdato': '1968-10-24',
                            'navn': {'fornavn': 'Anders', 'etternavn': 'Opedal'},
                            'erDoed': False
                        },
                        'fratradt': False,
                    }
                ]
            }
        ]
    }

@pytest.fixture
def sample_brreg_regnskap_response():
    """Real-format BRREG Regnskap response (simplified)."""
    return [
        {
            'journalnr': '2024123456',
            'regnskapsperiode': {'fraDato': '2023-01-01', 'tilDato': '2023-12-31'},
            'valuta': 'NOK',
            'regnskapstype': 'SELSKAP',
            'oppstillingsplan': 'store',
            'resultatregnskap': {
                'driftsresultat': {
                    'driftsinntekter': {
                        'salgsinntekter': 1200000000,
                        'sumDriftsinntekter': 1250000000
                    },
                    'driftskostnader': {
                        'lonnskostnad': 450000000,
                        'sumDriftskostnader': 1050000000
                    },
                    'driftsresultat': 200000000
                },
                'finansresultat': {
                    'finansinntekter': {'sumFinansinntekter': 30000000},
                    'finanskostnader': {'sumFinanskostnader': 50000000},
                    'nettoFinans': -20000000
                },
                'ordinaertResultatFoerSkattekostnad': 180000000,
                'skattekostnadPaaOrdinaertResultat': 39600000,
                'aarsresultat': 140400000
            },
            'eiendeler': {
                'sumEiendeler': 2500000000,
                'omloepsmidler': {
                    'bankinnskuddKontanterOgLignende': 350000000
                }
            },
            'egenkapitalGjeld': {
                'egenkapital': {'sumEgenkapital': 1200000000},
                'gjeld': {
                    'sumGjeld': 1300000000,
                    'langsiktigGjeld': {'sumLangsiktigGjeld': 800000000},
                    'kortsiktigGjeld': {'sumKortsiktigGjeld': 500000000}
                },
                'sumEgenkapitalGjeld': 2500000000
            }
        }
    ]

@pytest.fixture
def mock_budget_manager():
    from app.core.budget_manager import BudgetManager
    return BudgetManager(max_requests=2000)

@pytest.fixture
def mock_cache_manager():
    from app.core.cache_manager import CacheManager
    return CacheManager()

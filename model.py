from dataclasses import dataclass
from datetime import datetime

@dataclass()
class ADME:
    drug_id: str
    drug: str
    y: str
    dataset_type: str
    adme_type: str
    drug_type: str
    date_inserted: datetime

    table_name = dict(
        Distribution = 'distribution',
        Absorption = 'absorption',
        Metabolism = 'metabolism',
        Excretion = 'excreation'
    )

    schema = 'adme'

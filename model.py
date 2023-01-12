from dataclasses import dataclass
from datetime import datetime

@dataclass()
class ADME:
    '''
    Creating dataclass that defines table structure
    '''
    drug_id: str
    drug: str
    y: str
    dataset_type: str
    adme_type: str
    drug_type: str
    date_inserted: datetime

    # defining four different tables for ADME with same structure
    table_name = dict(
        Distribution = 'distribution',
        Absorption = 'absorption',
        Metabolism = 'metabolism',
        Excretion = 'excreation'
    )

    schema = 'adme'

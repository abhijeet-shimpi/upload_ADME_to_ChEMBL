'''
Creating a dictionary of List of ADME types
Can be further added to database for maintenance and clean operations
'''
adme_dict = dict(
    Distribution = ['BBB_Martins',
                    'PPBR_AZ',
                    'VDss_Lombardo'],
    Absorption = ['Caco2_Wang',
                  'PAMPA_NCATS',
                  'HIA_Hou',
                  'Pgp_Broccatelli',
                  'Bioavailability_Ma',
                  'Lipophilicity_AstraZeneca',
                  'Solubility_AqSolDB',
                  'HydrationFreeEnergy_FreeSolv'],
    Metabolism = ['CYP2C19_Veith',
                  'CYP2D6_Veith',
                  'CYP3A4_Veith',
                  'CYP1A2_Veith',
                  'CYP2C9_Veith',
                  'CYP2C9_Substrate_CarbonMangels',
                  'CYP2D6_Substrate_CarbonMangels',
                  'CYP3A4_Substrate_CarbonMangels'],
    Excretion = ['Half_Life_Obach',
                 'Clearance_Hepatocyte_AZ']
)
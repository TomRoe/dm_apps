from django.db import models
from django.utils.translation import gettext_lazy as _


YES_NO_UNKNOWN = (
    ('Yes', 'Yes'),
    ('No', 'No'),
    ('Unknown', 'Unknown'),
    ('Not Applicable', 'Not Applicable')
)

AGREEMENT_DATABASE = (
    ('APGIS', "APGIS - Aboriginal Programs and Governance Information System"),
    ('Unknown', "Unknown"),
    ('Not Applicable', "Not Applicable"),
    ('Other', "Other"),
)


FUNDING_SOURCES = (
    ('AFS', 'AFS – Aboriginal Fisheries Strategy'),
    ('AAROM', 'AAROM – Aboriginal Aquatic Resources and Oceans Management'),
    ('PST (TBG&C)',  'PST (TBG&C) – Pacific Salmon Treaty/Treasury Board Grants & Contributions'),
    ('Science',  'Science – Program funding redirected to a G&C agreement'),
    ('HSP', 'HSP – Habitat Stewardship Program'),
    ('BCSRIF', 'BCSRIF – British Columbia Salmon Restoration and Innovation Fund'),
    ('CNFASAR', 'CNFASAR – Canadian Nature Fund for Aquatic Species at Risk'),
    ('CRF', 'CRF – Coastal Restoration Fund'),
    ('FHRI', 'FHRI – Fisheries Habitat Restoration Initiative'),
    ('IHPP', 'IHPP – Indigenous Habitat Participation Program'),
    ('RFCPP', 'RFCPP – Recreational Fisheries Conservation Partnership Program'),
    ('PSSI', 'PSSI - Pacific Salmon Strategy Initiative'),
    ('AFSAR', 'AFSAR - Aboriginal Fund for Species at Risk'),
    ('SEP', 'SEP - Salmon Enhancement Program'),
    ('AHRF', 'AHRF - Aquatic Habitat Restoration Fund'),
    ('SSI', 'SSI- Salish Sea Initiative'),
    ('Other', 'Other – Add Name and Definition'),
    ('Unknown', 'Unknown'),
)

AGREEMENT_TYPE = (
    ('Formal Agreement', 'Formal Agreement'),
    ('Amendment', 'Amendment'),
    ('First Nations Treaty Agreement', 'First Nations Treaty Agreement'),
    ('Supply Arrangement', 'Supply Arrangement'),
    ('Contract', 'Contract'),
    ('Unknown', 'Unknown'),
    ('Not applicable', 'Not applicable'),
    ('Other', 'Other'),
)

LEAD_ORGANIZATION = (
    ('First Nations', 'First Nations'),
    ('DFO', 'DFO'),
    ('Collaborative', 'Collaborative'),
    ('Unknown', 'Unknown'),
    ('Not applicable', 'Not applicable'),
    ('Other', 'Other')
)

REGION= (
    ("Yukon", "Yukon/Transboundary"),
    ("NCA", "North Coast"),
    ("SCA", "South Coast"),
    ("FIA", "Fraser"),)


ECOSYSTEM_TYPE = (
    ('Freshwater', 'Freshwater'),
    ('Estuarine', 'Estuarine'),
    ('Marine', 'Marine'),
    ('Unknown', 'Unknown'),
    ('Not applicable', 'Not applicable'),
    ('Other', 'Other'),
)

SMU_NAME = (
    ('Barkley/Somass Sockeye Salmon', 'Barkley/Somass Sockeye Salmon'),
    ('Chum general', 'Chum general'),
    ('ECVI/Mainland Inlet Pink Salmon', 'ECVI/Mainland Inlet Pink Salmon'),
    ('ECVI/Mainland Inlet Sockeye Salmon', 'ECVI/Mainland Inlet Sockeye Salmon'),
    ('Inner South Coast Chum Salmon', 'Inner South Coast Chum Salmon'),
    ('JST/Mainland Inlet Chinook Salmon', 'JST/Mainland Inlet Chinook Salmon'),
    ('JST/Mainland Inlets Coho Salmon', 'JST/Mainland Inlets Coho Salmon'),
    ('Lower Strait of Georgia Chinook Salmon', 'Lower Strait of Georgia Chinook Salmon'),
    ('South Coast Sockeye General', 'South Coast Sockeye General'),
    ('Strait of Georgia Coho Salmon', 'Strait of Georgia Coho Salmon'),
    ('Upper Strait of Georgia Chinook Salmon', 'Upper Strait of Georgia Chinook Salmon'),
    ('WCVI Chinook Salmon', 'WCVI Chinook Salmon'),
    ('WCVI Chum Salmon', 'WCVI Chum Salmon'),
    ('WCVI Coho Salmon', 'WCVI Coho Salmon'),
    ('Unknown', 'Unknown'),
    ('Not applicable', 'Not applicable'),
    ('Other', 'Other'),
)

SPECIES = (
    ('CH', 'Chinook Salmon (Oncorhynchus tshawytscha)'),
    ('CM', 'Chum Salmon (Oncorhynchus keta)'),
    ('CO', 'Coho Salmon (Oncorhynchus kisutch)'),
    ('PK',  'Pink Salmon (Oncorhynchus gorbuscha)'),
    ('SK',  'Sockeye Salmon (Oncorhynchus nerka)'),
    ('SH', 'Steelhead (Oncorhynchus mykiss)'),
    ('Unknown', 'Unknown'),
    ('Not applicable', 'Not applicable'),
    ('Other', 'Other'),
)

SALMON_LIFE_CYCLE = (
    ('Adult', 'Adult – adult salmon residing in the ocean; or are migrating in the river.'),
    ('Juvenile', 'Juvenile – Fish in the fry, parr & smolt stage of life.'),
    ('Spawning', 'Spawning – a phase of the salmonid life cycle where male and female fish are in the spawning grounds, are mature and able to spawn.'),
    ('Incubation', 'Incubation – Inter-gravel development phase including the egg and alevin life cycle stages.'),
    ('Unknown', 'Unknown'),
    ('Not applicable', 'Not applicable'),
    ('Other', 'Other'),
)

PROJECT_STAGE = (
    ('Proposed', 'Proposed'),
    ('Developing', 'Developing'),
    ('Pilot', 'Pilot'),
    ('Active', 'Active'),
    ('Completed', 'Completed'),
    ('Terminated', 'Terminated'),
    ('Unknown', 'Unknown'),
    ('Not applicable', 'Not applicable'),
    ('Other', 'Other'),
)

PROJECT_TYPE = (
    ('Population Science', 'Population Science'),
    ('Habitat Science', 'Habitat Science'),
)

PROJECT_SUB_TYPE = (
    ('Research & Development', 'Research & Development'),
    ('Community', 'Community'),
    ('Monitoring', 'Monitoring'),
    ('Sampling', 'Sampling'),
    ('Recovery', 'Recovery'),
    ('Restoration', 'Restoration'),
    ('Design & Feasibility', 'Design & Feasibility'),
    ('Decommissioning', 'Decommissioning'),
    ('Implementation', 'Implementation'),
    ('Maintenance', 'Maintenance'),
    ('Stewardship', 'Stewardship'),
    ('Research & Monitoring', 'Research & Monitoring'),
    ('Unknown', 'Unknown'),
    ('Not applicable', 'Not applicable'),
)

MONITORING_APPROACH = (
    ('Indicator', 'Indicator'),
    ('Intensive', 'Intensive'),
    ('Extensive', 'Extensive'),
    ('Unknown', 'Unknown'),
    ('Not applicable', 'Not applicable'),
)

PROJECT_THEME = (
    ('Escapement', 'Escapement'),
    ('Conservation', 'Conservation'),
    ('Catch (First Nations)', 'Catch (First Nations)'),
    ('Catch (Recreational)', 'Catch (Recreational)'),
    ('Catch (Commercial)', 'Catch (Commercial)'),
    ('Enhancement', 'Enhancement'),
    ('Administration', 'Administration'),
    ('Habitat', 'Habitat'),
    ('Unknown', 'Unknown'),
    ('Not applicable', 'Not applicable'),
)

PROJECT_CORE_ELEMENT = (
    ('Planning', 'Planning'),
    ('Field Work', 'Field Work'),
    ('Sample Processing', 'Sample Processing'),
    ('Data Entry', 'Data Entry'),
    ('Data Analysis', 'Data Analysis'),
    ('Reporting', 'Reporting'),
)

SUPPORTIVE_COMPONENT = (
    ('Workshop', 'Workshop'),
    ('Data Collection', 'Data Collection'),
    ('Evaluation', 'Evaluation'),
    ('Assessment', 'Assessment'),
    ('Committee', 'Committee'),
    ('Administration', 'Administration'),
    ('Training', 'Training'),
    ('Staffing', 'Staffing'),
    ('Meeting', 'Meeting'),
    ('Computer Support', 'Computer Support'),
    ('Advice & Consultation', 'Advice & Consultation'),
    ('Study Design', 'Study Design'),
    ('Literature Review', 'Literature Review'),
    ('Equipment Support', 'Equipment Support'),
    ('Equipment Repair/Building', 'Equipment Repair/Building'),
    ('Analysis of Current Data', 'Analysis of Current Data'),
    ('Analysis of Historical Data', 'Analysis of Historical Data'),
    ('Analysis - Other', 'Analysis - Other'),
    ('Unknown', 'Unknown'),
    ('Not applicable', 'Not applicable'),
)

PROJECT_PURPOSE = (
    ('Biological',
    (('Population Estimates', 'Population Estimates'),
    ('Run Reconstruction', 'Run Reconstruction'),
    ('Biological Abundance Benchmarks', 'Biological Abundance Benchmarks'),
    ('Terminal Abundance', 'Terminal Abundance'),
    ('In-River Abundance', 'In-River Abundance'),
    ('Catch Estimates', 'Catch Estimates'),
    ('Smolt Abundance', 'Smolt Abundance'),
    ('Adult Abundance', 'Adult Abundance'),
    ('Administration', 'Administration'),
    ('Recovery', 'Recovery'),
    ('Rebuilding', 'Rebuilding'),
    ('Enhancement', 'Enhancement'))),

    ('Catch/Fisheries',
    (('Foods, Social and Ceremonial Fisheries', 'Foods, Social and Ceremonial Fisheries'),
    ('Fraser Recreational', 'Fraser Recreational'),
    ('Fraser Economic Opportunity (EO)', 'Fraser Economic Opportunity (EO)'),
    ('Fraser Commercial (in-river portions of Area', 'Fraser Commercial (in-river portions of Area'),
    ('29E (Gillnet) and Area 29B (Seine', '29E (Gillnet) and Area 29B (Seine)'),
    ('Fraser Test Fisheries (Albion, Qualark)', 'Fraser Test Fisheries (Albion, Qualark)'),
    ('Marine Fisheries', 'Marine Fisheries'),
    ('Juan de Fuca Recreational', 'Juan de Fuca Recreational'),
    ('West Coast Vancouver Island Recreational', 'West Coast Vancouver Island Recreational'),
    ('Northern British Columbia Recreational', 'Northern British Columbia Recreational'),
    ('West Coast Vancouver Island Commercial', 'West Coast Vancouver Island Commercial'),
    ('Troll', 'Troll'),
    ('Northern BC Commercial Troll', 'Northern BC Commercial Troll'),
    ('Taaq-wiihak', 'Taaq-wiihak'),
    ('Fish Passage', 'Fish Passage'))),

    ('Habitat',
    (('Water Levels', 'Water Levels'),
    ('Riparian', 'Riparian'),
    ('Estuarine', 'Estuarine'),
    ('Nearshore & Marine', 'Nearshore & Marine'),
    ('Instream Structure', 'Instream Structure'),
    ('Floodplain connectivity', 'Floodplain connectivity'),
    ('Watershed', 'Watershed'),
    ('Nutrient Supplementation', 'Nutrient Supplementation'),
    ('Habitat Condition', 'Habitat Condition'),
    ('Unknown', 'Unknown'),
    ('Not applicable', 'Not applicable'),
    ('Other', 'Other'))),
)

DFO_LINK = (
    ('Fisheries Management', 'Fisheries Management'),
    ('Commercial Fisheries', 'Commercial Fisheries'),
    ('Recreational Fisheries', 'Recreational Fisheries'),
    ('Aboriginal Prog. & Treat', 'Aboriginal Prog. & Treat'),
    ('Aquaculture Management', 'Aquaculture Management'),
    ('Salmonid Enhancement', 'Salmonid Enhancement'),
    ('International Engagement', 'International Engagement'),
    ('Small Craft Harbours', 'Small Craft Harbours'),
    ('Conservation & Protection', 'Conservation & Protection'),
    ('Air Surveillance', 'Air Surveillance'),
    ('Aquatic Animal Health', 'Aquatic Animal Health'),
    ('Biotechnology & Genomics', 'Biotechnology & Genomics'),
    ('Aquaculture Science', 'Aquaculture Science'),
    ('Fisheries Science', 'Fisheries Science'),
    ('Fish and Seafood Sector', 'Fish and Seafood Sector'),
    ('Fish & Fish Habitat Prot.', 'Fish & Fish Habitat Prot.'),
    ('Aquatic Invasive Species', 'Aquatic Invasive Species'),
    ('Species at Risk', 'Species at Risk'),
    ('Marine Planning & Conser.', 'Marine Planning & Conser.'),
    ('Aquatic Ecosystem Science', 'Aquatic Ecosystem Science'),
    ('Oceans & Clim. Chng. Sci.', 'Oceans & Clim. Chng. Sci.'),
    ('Waterways Management', 'Waterways Management'),
    ('Environmental Response', 'Environmental Response'),
    ('Unknown', 'Unknown'),
    ('Not applicable', 'Not applicable'),
)

GOVERNMENT_LINK = (
    ('Municipality', 'Municipality'),
    ('Province of British Columbia', 'Province of British Columbia'),
    ('Yukon Territory', 'Yukon Territory'),
    ('ENVIRONMENT CANADA', 'Environment Canada'),
    ('Climate Change Canada', 'Climate Change Canada'),
    ('Alaska Department of Fish & Game', 'Alaska Department of Fish & Game'),
    ('Washington State', 'Washington State'),
    ('Unknown', 'Unknown'),
    ('Not Applicable', 'Not Applicable'),
    ('Other', 'Other'),
)

ROLE = (
    ('Chief', 'Chief'),
    ('Biologist', 'Biologist'),
    ('Aquatics Manager', 'Aquatics Manager'),
    ('Technician', 'Technician'),
    ('Director', 'Director'),
    ('Fisheries Manager', 'Fisheries Manager'),
    ('Refuge Manager', 'Refuge Manager'),
    ('Scientist', 'Scientist'),
    ('Stewardship Director', 'Stewardship Director'),
    ('Unknown', 'Unknown'),
    ('Other', 'Other'),
)

COUNTRY_CHOICES = (
    ('Canada', 'Canada'),
    ('United States of America', 'United States of America'),
)

PROVINCE_STATE_CHOICES = (
    ('Alberta', 'Alberta'),
    ('British Columbia', 'British Columbia'),
    ('Manitoba', 'Manitoba'),
    ('New Brunswick', 'New Brunswick'),
    ('Newfoundland & Labrador', 'Newfoundland & Labrador'),
    ('Nova Scotia', 'Nova Scotia'),
    ('Ontario', 'Ontario'),
    ('Prince Edward Island', 'Prince Edward Island'),
    ('Quebec', 'Quebec'),
    ('Saskatchewan', 'Saskatchewan'),
    ('Northwest Territories', 'Northwest Territories'),
    ('Nunavut', 'Nunavut'),
    ('Yukon', 'Yukon'),
    ('Washington', 'Washington'),
    ('Alaska', 'Alaska'),
    ('Oregon', 'Oregon'),
)

ORGANIZATION_TYPE = (
    ('First Nation', 'First Nation'),
    ('Company', 'Company'),
    ('Government', 'Government'),
    ('Non-Profit Organization', 'Non-Profit Organization'),
    ('University', 'University'),
)

PLANNING_METHOD = (
    ('Feasibility Study', 'Feasibility Study'),
    ('Project Design', 'Project Design'),
    ('Resource Allocation', 'Resource Allocation'),
    ('Objective-Setting', 'Objective-Setting'),
    ('Other', 'Other'),
)

FIELD_WORK = (
    ('Biological - Visual',
    (('Stream Walks', 'Stream Walks'),
    ('Boat Survey', 'Boat Survey'),
    ('Snorkle Survey', 'Snorkle Survey'),
    ('Raft', 'Raft'),
    ('Deadpitch', 'Deadpitch'),
    ('Microtrolling', 'Microtrolling'),
    ('Roving', 'Roving'),
    ('Fishwheel', 'Fishwheel'),
    ('Electrofishing', 'Electrofishing'))),

    ('Biological - Intensive Measure',
    (('Weir', 'Weir'),
    ('Fence', 'Fence'),
    ('Fishway-Tunnels', 'Fishway-Tunnels'))),

    ('Biological - Instrumentation',
    (('Sonar', 'Sonar'),
    ('DIDSON', 'DIDSON'),
    ('Video', 'Video'),
    ('Hydroacoustic', 'Hydroacoustic'),
    ('Resistivity', 'Resistivity'),
    ('River Surveyor', 'River Surveyor'))),

    ('Biological - Tagging',
    (('Pit', 'Pit'),
    ('Coded Wire Tag', 'Coded Wire Tag'),
    ('Hallprint', 'Hallprint'),
    ('Spaghetti', 'Spaghetti'),
    ('Radio', 'Radio'))),

    ('Biological - Biodata',
    (('Size', 'Size'),
    ('Sex', 'Sex'),
    ('Age', 'Age'),
    ('DNA (Genetic Stock ID)', 'DNA (Genetic Stock ID)'),
    ('Otoliths', 'Otoliths'),
    ('Health Condition', 'Health Condition'))),

    ('Biological - Aerial',
    (('Plane', 'Plane'),
    ('Helicopter', 'Helicopter'),
    ('Drone', 'Drone'))),

    ('Biological - Catch',
    (('Creel', 'Creel'),
    ('Other', 'Other'))),

    ('Biological - Trapping',
    (('Smolt', 'Smolt'),
    ('Seines', 'Seines'),
    ('Gill Netting', 'Gill Netting'))),

    ('Biological - Enhancement',
    (('Broodstock Take', 'Broodstock Take'),
    ('Other', 'Other'))),

    ('Field Work - Habitat',
    (('Physical Analysis', 'Physical Analysis'),
    ('Chemical Analysis', 'Chemical Analysis'),
    ('Plankton', 'Plankton'),
    ('Riparian', 'Riparian'),
    ('Other', 'Other'))),

    ('Habitat - Restoration',
    (('Aerial Surveys', 'Aerial Surveys'),
    ('eDNA', 'eDNA'),
    ('Electofishing', 'Electofishing'),
    ('Hydrological modelling', 'Hydrological modelling'),
    ('Invasive Species Surveys', 'Invasive Species Surveys'),
    ('Physical Habitat Surveys', 'Physical Habitat Surveys'),
    ('Vegetation Surveys', 'Vegetation Surveys'),
    ('Nets and Traps', 'Nets and Traps'),
    ('Photo Point Monitoring', 'Photo Point Monitoring'),
    ('PIT Tagging and Telemetry', 'PIT Tagging and Telemetry'),
    ('Snorkle Surveys', 'Snorkle Surveys'),
    ('Temperature Loggers', 'Temperature Loggers'),
    ('Hydrometer Installments', 'Hydrometer Installments'),
    ('Water Sampling', 'Water Sampling'),
    ('Qualitative Visual assessment', 'Qualitative Visual assessment'),
    ('Other', 'Other'))),
)

SAMPLE_PROCESSING = (
    ('Aging', 'Aging'),
    ('DNA (Genetic Stock ID)', 'DNA (Genetic Stock ID)'),
    ('Instrument Data Processing', 'Instrument Data Processing'),
    ('Scales', 'Scales'),
    ('Otoliths', 'Otoliths'),
    ('DNA', 'DNA'),
    ('Heads', 'Heads'),
    ('Other', 'Other'),
)

DATA_ENTRY = (
    ('Direct entry into computer', 'Direct entry into computer'),
    ('Direct entry into database', 'Direct entry into database'),
    ('Direct entry into database', 'Paper, Followed by Entry into Computer'),
    ('Unknown', 'Unknown'),
    ('Not applicable', 'Not applicable'),
    ('Other', 'Other'),
)

METHOD_DOCUMENT = (
    ('Program Document', 'Program Document'),
    ('Administration Document', 'Administration Document'),
    ('Conference', 'Conference'),
    ('Book', 'Book'),
    ('CSAS', 'CSAS'),
    ('Contract', 'Contract'),
    ('Statement of Work', 'Statement of Work '),
    ('Training Document', 'Training Document'),
    ('Protocol', 'Protocol'),
    ('Field Notes', 'Field Notes'),
    ('Journal Article', 'Journal Article'),
    ('Guidance Document', 'Guidance Document'),
)

SAMPLES_COLLECTED = (

    ('Biological',
    (('FISH COUNTS', 'Fish Counts (fence, catch, static)'),
    ('ESCAPEMENT ESTIMATE', 'Escapement Estimate (non-expanded)'),
    ('Spawning Density', 'Spawning Density'),
    ('Broodstock Removal', 'Broodstock Removal'),
    ('Fish at Location (by segment or area)', 'Fish at Location (by segment or area)'),
    ('Spawning Location', 'Spawning Location'),
    ('Migration Timing', 'Migration Timing'),
    ('Length', 'Length'),
    ('Clip Status', 'Clip Status'),
    ('Tag Status', 'Tag Status'),
    ('Head Collection', 'Head Collection'),
    ('Scale Samples ', 'Scale Samples '),
    ('Smear Samples', 'Smear Samples'),
    ('Otoliths', 'Otoliths'),
    ('Other', 'Other'))),

    ('Habitat',
    (('Dissolved Oxygen', 'Dissolved Oxygen'),
    ('Temperature', 'Temperature'),
    ('Salinity', 'Salinity'),
    ('Water Flow', 'Water Flow'),
    ('Turbidity', 'Turbidity'),
    ('Weather conditions', 'Weather conditions'),
    ('Zooplankton', 'Zooplankton'),
    ('Invertebrates', 'Invertebrates'),
    ('Other', 'Other'))),

    ('Restoration',
    (('Aerial Surveys', 'Aerial Surveys'),
    ('eDNA', 'eDNA'),
    ('Electrofishing', 'Electrofishing'),
    ('Hydrological Modelling', 'Hydrological Modelling'),
    ('Invasive Species Surveys', 'Invasive Species Surveys'),
    ('Physical Habitat Surveys', 'Physical Habitat Surveys'),
    ('Vegetation Surveys', 'Vegetation Surveys'),
    ('Nets and Traps', 'Nets and Traps'),
    ('Photo Point Monitoring', 'Photo Point Monitoring'),
    ('PIT Tagging and Telemetry', 'PIT Tagging and Telemetry'),
    ('Snorkel Surveys', 'Snorkel Surveys'),
    ('Temperature Loggers', 'Temperature Loggers'),
    ('Hydrometer Installments', 'Hydrometer Installments'),
    ('Water Sampling', 'Water Sampling'),
    ('Qualitative Visual Assessment', 'Qualitative Visual Assessment'),
    ('Other', 'Other'))),
)

DATABASE = (
    ('ADF&G Zander', 'ADF&G Zander'),
    ('PSMFC CWT', 'PSMFC CWT'),
    ('ADF&G Region 1', 'ADF&G Region 1'),
    ('ADF&G CWT Online Release', 'ADF&G CWT Online Release'),
    ('ADF&G SF Research and Technical Services', 'ADF&G SF Research and Technical Services'),
    ('NuSEDs', 'NuSEDs'),
    ('iREC', 'iREC'),
    ('KREST', 'KREST'),
    ('First Nations Databases', 'First Nations Databases'),
    ('Shared DFO Drives', 'Shared DFO Drives'),
    ('First Nations Harvest (AHMS)', 'First Nations Harvest (AHMS)'),
    ('Fishery Operations System (FOS)', 'Fishery Operations System (FOS)'),
    ('Mark Recovery Program (MRPRO)', 'Mark Recovery Program (MRPRO)'),
    ('Clockwork', 'Clockwork'),
    ('Biodatabase (South Coast DFO)', 'Biodatabase (South Coast DFO)'),
    ('PADS', 'PADS'),
    ('Otomanager', 'Otomanager'),
    ('Pacific Salmon Commission', 'Pacific Salmon Commission'),
    ('Genetics Group (PBS)', 'Genetics Group (PBS)'),
    ('Individual Computer', 'Individual Computer'),
    ('Pacific States Marine Fisheries Commission (www.rmpc.org)', 'Pacific States Marine Fisheries Commission (www.rmpc.org)'),
    ('Central Coast FSC Catch', 'Central Coast FSC Catch'),
    ('Private', 'Private'),
    ('PIT Tag Information System (PTAGIS)', 'PIT Tag Information System (PTAGIS)'),
    ('Not Applicable', 'Not Applicable'),
    ('Other', 'Other'),
)

SAMPLE_BARRIER = (
    ('Weather', 'Weather'),
    ('Site Access', 'Site Access'),
    ('Equipment Failure', 'Equipment Failure'),
    ('Equipment Not Available', 'Equipment Not Available'),
    ('Staffing Unavailable', 'Staffing Unavailable'),
    ('Staffing Not Trained', 'Staffing Not Trained'),
    ('Unknown', 'Unknown'),
    ('Not Applicable', 'Not Applicable'),
    ('Other', 'Other'),
)

DATA_BARRIER = (
    ('No Person Available', 'No Person Available'),
    ('Sample Data Requires More Work Before it can be Entered into Database', 'Sample Data Requires More Work Before it can be Entered into Database'),
    ('Person Available but Lack of Training', 'Person Available but Lack of Training'),
    ('Equipment is Available but not Working', 'Equipment is Available but not Working'),
    ('Equipment is not Available', 'Equipment is not Available'),
    ('IT Issues', 'IT Issues'),
    ('Network Connection Issues', 'Network Connection Issues'),
    ('UNKNOWN', 'Unknown'),
    ('Not Applicable', 'Not Applicable'),
    ('Other', 'Other'),
)

SAMPLE_FORMAT = (
    ('Excel', 'Excel'),
    ('Paper', 'Paper'),
    ('Log Books', 'Log Books'),
    ('Word', 'Word'),
    ('PDF Files', 'PDF Files'),
    ('SIL-Hardcopy', 'SIL-Hardcopy'),
    ('SIL-Digitized', 'SIL-Digitized'),
    ('Instrument Files', 'Instrument Files'),
    ('Database Filed', 'Database Filed'),
    ('SENS', 'SENS'),
    ('Wet Notes', 'Wet Notes'),
    ('Not Applicable', 'Not Applicable'),
    ('Other', 'Other'),
)

DATA_PRODUCTS = (
    ('Relative Abundance', 'Relative Abundance'),
    ('Escapement Estimate – Expanded/Final', 'Escapement Estimate – Expanded/Final'),
    ('Escapement Estimate – Unexpanded/Preliminary', 'Escapement Estimate – Unexpanded/Preliminary'),
    ('Habitat Data', 'Habitat Data'),
    ('Harvest Rate', 'Harvest Rate'),
    ('Stock Recruitment', 'Stock Recruitment'),
    ('Survival Rate', 'Survival Rate'),
    ('Marked Status', 'Marked Status'),
    ('Proportion of Sampled Fish Effort/Time', 'Proportion of Sampled Fish Effort/Time'),
    ('Proportion of In-River Salmon Destined for Spawning', 'Proportion of In-River Salmon Destined for Spawning'),
    ('Sex Composition', 'Sex Composition'),
    ('Age Composition Data', 'Age Composition Data'),
    ('Stock Composition (GSI / DNA)Data', 'Stock Composition (GSI / DNA)Data'),
    ('Condition of Fish (DNA Based)', 'Condition of Fish (DNA Based)'),
    ('Ratio of Catchability', 'Ratio of Catchability'),
    ('Other', 'Other'),
)

DATA_PROGRAMS = (
    ('R', 'R'),
    ('VidEsc', 'VidEsc'),
    ('Stratified Population Analysis System', 'Stratified Population Analysis System'),
    ('Bayesian Time Stratified Petersen Analysis System', 'Bayesian Time Stratified Petersen Analysis System'),
    ('Microsoft Excel', 'Microsoft Excel'),
)

DATA_COMMUNICATION = (
    ('Presentations', 'Presentations'),
    ('Workshops', 'Workshops'),
    ('Reports', 'Reports'),
    ('Data Summaries', 'Data Summaries'),
    ('Bulletins', 'Bulletins'),
    ('Unknown', 'Unknown'),
    ('Not Applicable', 'Not Applicable'),
    ('Other', 'Other'),
)

REPORT_TIMELINE = (
    ('Progress Report', 'Progress Report'),
    ('Final Report', 'Final Report'),
    ('Not Applicable', 'Not Applicable'),
    ('Other', 'Other'),
)

REPORT_TYPE = (
    ('Project', 'Project'),
    ('Catch', 'Catch'),
    ('Population', 'Population'),
    ('Sampling', 'Sampling'),
    ('Methods', 'Methods'),
    ('Habitat', 'Habitat'),
    ('Recovery', 'Recovery'),
    ('Enhancement', 'Enhancement'),
    ('R&D', 'R&D'),
    ('Administration', 'Administration'),
)

KEY_ELEMENT = (
    ('A', 'A'),
    ('B', 'B'),
    ('C', 'B'),
    ('D', 'D'),
    ('OTHER', 'Other'),
)

ACTIVITY_NUMBER = (
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
    ('4', '4'),
    ('5', '5'),
    ('6', '6'),
    ('7', '7'),
    ('8', '8'),
    ('9', '9'),
    ('10', '10'),
    ('11', '11'),
    ('12', '12'),
    ('13', '13'),
    ('14', '14'),
    ('15', '15'),
    ('16', '16'),
    ('17', '17'),
    ('18', '18'),
    ('19', '19'),
    ('20', '20'),
    ('OTHER', 'Other'),
)

SAMPLE_TYPE_OUTCOMES = (
    ('Biological',
    (('Adipose Clips', 'Adipose Clips'),
    ('Age', 'Age'),
    ('Catch Monitoring (Counts)', 'Catch Monitoring (Counts)'),
    ('Catch Effort', 'Catch Effort'),
    ('Auxiliary Appendage Clips', 'Auxiliary Appendage Clips'),
    ('CWT Tagging', 'CWT Tagging'),
    ('CWT Recovery(Heads)', 'CWT Recovery(Heads)'),
    ('Count(Enumeration)', 'Count(Enumeration)'),
    ('DNA(for Genetic Stock Identification)', 'DNA(for Genetic Stock Identification)'),
    ('Fish Clips', 'Fish Clips'),
    ('Health Condition', 'Health Condition'),
    ('Size', 'Size'),
    ('PIT Tagging', 'PIT Tagging'),
    ('PIT Recovery', 'PIT Recovery'),
    ('Otoliths', 'Otoliths'),
    ('Sea Lice Counts', 'Sea Lice Counts'),
    ('Secondary Marks', 'Secondary Marks'),
    ('Sex', 'Sex'),
    ('Spaghetti Tagging', 'Spaghetti Tagging'),
    ('Spaghetti Tag Recovery', 'Spaghetti Tag Recovery'),
    ('Spawning Success', 'Spawning Success'),
    ('Species Composition', 'Species Composition'),
    ('Tag Loss Data', 'Tag Loss Data'),
    ('Tissue Collection (Disease)', 'Tissue Collection (Disease)'),
    ('Egg Characteristics', 'Egg Characteristics'),
    ('Enhancement', 'Enhancement'),
    ('Brood Collection', 'Brood Collection'),
    ('Other', 'Other'))),

    ('Habitat - Monitoring',
    (('Temperature', 'Temperature'),
    ('Water Quality', 'Water Quality'),
    ('Water Flow', 'Water Flow'),
    ('Stream Debris', 'Stream Debris'),
    ('Plankton', 'Plankton'),
    ('Other', 'Other'))),

    ('Habitat - Restoration',
    (('Fish Passage', 'Fish Passage'),
    ('Water Levels', 'Water Levels'),
    ('Riparian', 'Riparian'),
    ('Estuarine', 'Estuarine'),
    ('Nearshore Marine', 'Nearshore Marine'),
    ('Instream Structure', 'Instream Structure'),
    ('Floodplain Connectivity', 'Floodplain Connectivity'),
    ('Watershed', 'Watershed'),
    ('Nutrient Supplementation', 'Nutrient Supplementation'),
    ('Other', 'Other'))),
)

OUTCOMES = (
    ('Submitted Samples', 'Submitted Samples'),
    ('Live Collection', 'Live Collection'),
    ('Summarized Data', 'Summarized Data'),
    ('Raw Data', 'Raw Data'),
    ('Stream Inspection Log', 'Stream Inspection Log'),
    ('Analyzed Data - Non-Expanded Estimates', 'Analyzed Data - Non-Expanded Estimates'),
    ('Analyzed Data - Expanded Estimates', 'Analyzed Data - Expanded Estimates'),
    ('Analyzed Data - Other', 'Analyzed Data - Other'),
    ('Annual Stream Report', 'Annual Stream Report'),
    ('Report Document', 'Report Document'),
    ('Summary of Activities', 'Summary of Activities'),
    ('Meeting Summary', 'Meeting Summary'),
    ('Other', 'Other'),
)

CAPACITY = (
    ('NEW TRAINING', 'New Training'),
    ('NEW STAFF INTEREST', 'New staff interest'),
    ('VOLUNTEERS SHOWED INTEREST', 'Volunteers showed interest'),
    ('COMMUNITY CONNECTIONS MADE', 'Community connections made'),
    ('PUBLIC ENGAGEMENT', 'Public engagement'),
    ('PREVIOUS STAFF TRAINING UPGRADED', 'Previous Staff Training upgraded'),
    ('EQUIPMENT RESOURCES IMPROVED', 'Equipment resources improved'),
    ('IMPROVED FISHERIES KNOWLEDGE AMONG COMMUNITY', 'Improved fisheries knowledge among community'),
    ('IMPROVED COMMUNICATION BETWEEN DFO AND FUNDING RECIPIENT', 'Improved communication between DFO and funding recipient'),
)

DATA_QUALITY = (
    ('Level 1 (Very High Quality)', 'Level 1 (Very High Quality)'),
    ('LEVEL 2 (High Quality)', 'LEVEL 2 (High Quality)'),
    ('Level 3 (Good Quality)', 'Level 3 (Good Quality)'),
    ('Level 4 (Moderate Quality)', 'Level 4 (Moderate Quality)'),
    ('Level 5 (Low Quality)', 'Level 5 (Low Quality)'),
    ('Unknown', 'Unknown'),
    ('Not Applicable', 'Not Applicable'),
)

OUTCOME_BARRIER = (
    ('Site Access', 'Site Access'),
    ('Equipment Failure', 'Equipment Failure'),
    ('Equipment not Available', 'Equipment not Available'),
    ('Staffing Unavailable', 'Staffing Unavailable'),
    ('Staffing not Trained', 'Staffing not Trained'),
    ('Weather', 'Weather'),
)

SUBJECT = (
    ('People', 'People'),
    ('Projects', 'Projects'),
    ('Objectives', 'Objectives'),
    ('Methods', 'Methods'),
    ('Data', 'Data'),
    ('Organizations', 'Organizations'),
    ('Other', 'Other'),
)

FN_COMMUNICATIONS = (
    ('Presentations', 'Presentations'),
    ('Workshops', 'Workshops'),
    ('Reports', 'Reports'),
    ('Data Summaries', 'Data Summaries'),
    ('Bulletins', 'Bulletins'),
    ('Other', 'Other'),
    ('Not Applicable', 'Not Applicable'),
)

ELEMENT_TITLE = (
    ('Aquatic Resource Management and Stewardship', 'Aquatic Resource Management and Stewardship'),
    ('Food, Social and Ceremonial (FSC) Fisheries Manangement', 'Food, Social and Ceremonial (FSC) Fisheries Manangement'),
    ('Economic Opportunities', 'Economic Opportunities'),
    ('Aquatic Resource Management Compliance and Accountability', 'Aquatic Resource Management Compliance and Accountability'),
)

FUNDING_YEARS = (
    ('1950', '1950'),
    ('1951', '1951'),
    ('1952', '1952'),
    ('1953', '1953'),
    ('1954', '1954'),
    ('1955', '1955'),
    ('1956', '1956'),
    ('1957', '1957'),
    ('1958', '1958'),
    ('1959', '1959'),
    ('1960', '1960'),
    ('1961', '1961'),
    ('1962', '1962'),
    ('1963', '1963'),
    ('1964', '1964'),
    ('1965', '1965'),
    ('1966', '1966'),
    ('1967', '1967'),
    ('1968', '1968'),
    ('1969', '1969'),
    ('1970', '1970'),
    ('1971', '1971'),
    ('1972', '1972'),
    ('1973', '1973'),
    ('1974', '1974'),
    ('1975', '1975'),
    ('1976', '1976'),
    ('1977', '1977'),
    ('1978', '1978'),
    ('1979', '1979'),
    ('1980', '1980'),
    ('1981', '1981'),
    ('1982', '1982'),
    ('1983', '1983'),
    ('1984', '1984'),
    ('1985', '1985'),
    ('1986', '1986'),
    ('1987', '1987'),
    ('1988', '1988'),
    ('1989', '1989'),
    ('1990', '1990'),
    ('1991', '1991'),
    ('1992', '1992'),
    ('1993', '1993'),
    ('1994', '1994'),
    ('1995', '1995'),
    ('1996', '1996'),
    ('1997', '1997'),
    ('1998', '1998'),
    ('1999', '1999'),
    ('2000', '2000'),
    ('2001', '2001'),
    ('2002', '2002'),
    ('2003', '2003'),
    ('2004', '2004'),
    ('2005', '2005'),
    ('2006', '2006'),
    ('2007', '2007'),
    ('2008', '2008'),
    ('2009', '2009'),
    ('2010', '2010'),
    ('2011', '2011'),
    ('2012', '2012'),
    ('2013', '2013'),
    ('2014', '2014'),
    ('2015', '2015'),
    ('2016', '2016'),
    ('2017', '2017'),
    ('2018', '2018'),
    ('2019', '2019'),
    ('2020', '2020'),
    ('2021', '2021'),
    ('2022', '2022'),
    ('2023', '2023'),
    ('2024', '2024'),
    ('2025', '2025'),
    ('2026', '2026'),
    ('2027', '2027'),
    ('2028', '2028'),
    ('2029', '2029'),
    ('2030', '2030'),
    ('2031', '2031'),
    ('2032', '2032'),
    ('2033', '2033'),
    ('2034', '2034'),
    ('2035', '2035'),
    ('2036', '2036'),
    ('2037', '2037'),
    ('2038', '2038'),
    ('2039', '2039'),
    ('2040', '2040'),
    ('2041', '2041'),
    ('2042', '2042'),
    ('2043', '2043'),
    ('2044', '2044'),
    ('2045', '2045'),
    ('2046', '2046'),
    ('2047', '2047'),
    ('2048', '2048'),
    ('2049', '2049'),
    ('2050', '2050'),
)

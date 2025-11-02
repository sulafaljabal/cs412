# voter_analytics/models.py
# Sulaf Al Jabal (U78815065) 10/30/2025
# File description: models.py file, defining voter object 
from django.db import models

# Create your models here.


class Voter(models.Model):
    '''
    Store/represent the data from one runner at the Chicago Marathon 2023.
    BIB,First Name,Last Name,CTZ,City,State,Gender,Division,
    Place Overall,Place Gender,Place Division,Start TOD,Finish TOD,Finish,HALF1,HALF2
    '''

    # identification
    # voter_id = models.TextField() # this is themprimary key
    
    last_name = models.TextField()
    first_name = models.TextField()
    address_street_number = models.TextField()
    address_street_name = models.TextField()
    address_apartment_number = models.TextField()
    address_zip_code = models.IntegerField()
    date_of_birth = models.DateField()
    registration_date = models.DateField()
    party_affiliation = models.TextField()
    precint_number = models.TextField()
    v20state = models.BooleanField()
    v21town = models.BooleanField()
    v21primary = models.BooleanField()
    v22general = models.BooleanField()
    v23town = models.BooleanField()
    voter_score = models.IntegerField()
    

    def __str__(self):
        '''Return a string representation of this model instance.'''
        return f'{self.last_name}, {self.first_name}, {self.party_affiliation},{self.voter_score}'
    #end string representation

        
def load_data():
    '''Function to load data records from CSV file into Django model instances.'''
    
    Voter.objects.all().delete()
    filename = "/Users/sulaf/Documents/Boston Uni/Classes/Senior/DS 412/newton_voters.csv"
    f = open(filename)
    f.readline() # discard headers


    for line in f:
        line = line.strip()
        fields = line.split(',')
    
        try:
            # create a new instance of Result object with this record from CSV
            voter = Voter(
                            last_name=fields[1],
                            first_name=fields[2],
                            address_street_number = fields[3],
                            address_street_name = fields[4],
                            address_apartment_number = fields[5],
                            
                            address_zip_code = fields[6],
                            date_of_birth = fields[7],

                            registration_date = fields[8],
                            party_affiliation = fields[9].strip(),
                            precint_number = fields[10],
                        
                            v20state = fields[11].upper() == 'TRUE',
                            v21town = fields[12].upper() == 'TRUE',
                            v21primary = fields[13].upper() == 'TRUE',
                            v22general = fields[14].upper() == 'TRUE',
                            v23town = fields[15].upper() == 'TRUE',
                            voter_score = fields[16],
                        )
        


            voter.save() # commit to database
            # print(f'Created result: {voter}')
            
        except Exception as e:
            print(f"Skipping line due to exception: {e}")
    
    print(f'Done. Created {len(Voter.objects.all())} Voters.')

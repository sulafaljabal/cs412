# voter_analytics/views.py
# Sulaf Al Jabal (U78815065) 10/31/25
# File description: views for voter_analytics application

from django.shortcuts import render

# Create your views here.
from django.db.models.query import QuerySet
from django.views.generic import ListView, DetailView
from . models import *

import plotly.graph_objs as go
from plotly.offline import plot
 
class VoterListView(ListView):
    '''View to display voter statistics'''
 
    template_name = 'voter_analytics/voter.html'
    model = Voter
    context_object_name = 'voters'

    paginate_by = 100
 
    def get_queryset(self):

        voters = Voter.objects.all() # for now?
        
        # fields to filter by: party affiliation, minimum and maximum birth date (drop down list by calendar year ), voter score
        # whether or not they voted in certain elections 
        # need to have mixture of filters as well
        # party = self.request.GET.get('party_affiliation')
        print(self.request.GET)

        request_dict = self.request.GET
        print(f"Request dictionary: {request_dict}")

        if 'party_affiliation' in self.request.GET:
            party_affiliation = request_dict['party_affiliation']
            if party_affiliation and len(party_affiliation)!= 0:
                print(f"Party affiliation: {party_affiliation}")
                voters = voters.filter(party_affiliation=party_affiliation)
            #endif

        if 'v20state' in request_dict:
            v20state = request_dict['v20state']
            if v20state:
                voters = voters.filter(v20state=True)
            #endif

        if 'v21town' in request_dict:
            v21town = request_dict['v21town']
            if v21town:
                voters = voters.filter(v21town=True)
            #endif
        #endif

        if 'v21primary' in request_dict:
            v21primary = request_dict['v21primary']
            if v21primary:
                voters = voters.filter(v21primary=True)
            #endif

        if 'v22general' in request_dict:
            v22general = request_dict['v22general']
            if v22general:
                voters = voters.filter(v22general=True)
            #endif
        #endif

        if 'v23town' in request_dict:
            v23town = request_dict['v23town']
            if v23town:
                voters = voters.filter(v23town=True)
            #endif
        #endif
        
        if 'voter_score' in request_dict:
            voter_score = request_dict['voter_score']
            if voter_score != "":
                voters = voters.filter(voter_score=int(voter_score))
            #endif
        #endif

        #date_of_birth__gte=int(min_year)
        if 'min_birth_year' in request_dict:
            min_birth_year = request_dict['min_birth_year']
            if min_birth_year and min_birth_year != "":
                voters = voters.filter(date_of_birth__gte=f"{min_birth_year}-01-01")
            #endif
        #endif

        if 'max_birth_year' in request_dict:
            max_birth_year = request_dict['max_birth_year']
            if max_birth_year and max_birth_year != "":
                voters = voters.filter(date_of_birth__lte=f"{max_birth_year}-12-31")
            #endif
            # print(f"Max birth year present? {max_birth_year}")
        #endif
        print(f"Number of results: {len(voters)}")

        return voters
        #
    #enddef get _query set

    # get context data - need to add party affiliation, all individual 5 elections and 
    # voter scores (range)
    # birth years (range)
    def get_context_data(self, **kwargs):
        """ adding birth years, voter score, and party affiliations tp context object"""

        context = super().get_context_data(**kwargs)
        parties = Voter.objects.values_list('party_affiliation', flat=True).distinct().order_by('party_affiliation') 
        # for drop down
        party_affiliation_list = []

        for p in parties:
            if p: 
                party_affiliation_list.append(p) # in case of any whitespace
            #endif
        #endfor 
        print(f"Party affiliation list: {party_affiliation_list}")
        context['party_affiliation'] = party_affiliation_list
        context['birth_years'] = range(1900, 2025)
        context['voter_score'] = range(0,6)
        return context
#endc;ass

class VoterDetailView(DetailView):

    template_name = 'voter_analytics/voter_detail.html'
    model = Voter
    context_object_name = 'voter'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        voter = self.object
        link = f"https://www.google.com/maps/search/?api=1&query={voter.address_street_number}+{voter.address_street_name.replace(" ", "+")}+{voter.address_apartment_number}+Newton+MA+{voter.address_zip_code}"
        print(f"Link: {link}")
        context['address'] = link
        return context

class GraphsListView(ListView):
    template_name= "voter_analytics/graphs.html"
    model = Voter 
    context_object_name = 'v'

    def get_queryset(self):

        voters = Voter.objects.all() # for now?
        
        # fields to filter by: party affiliation, minimum and maximum birth date (drop down list by calendar year ), voter score
        # whether or not they voted in certain elections 
        # need to have mixture of filters as well
        # party = self.request.GET.get('party_affiliation')
        print(self.request.GET)

        request_dict = self.request.GET
        print(f"Request dictionary: {request_dict}")

        if 'party_affiliation' in self.request.GET:
            party_affiliation = request_dict['party_affiliation']
            if party_affiliation and len(party_affiliation)!= 0:
                print(f"Party affiliation: {party_affiliation}")
                voters = voters.filter(party_affiliation=party_affiliation)
            #endif

        if 'v20state' in request_dict:
            v20state = request_dict['v20state']
            if v20state:
                voters = voters.filter(v20state=True)
            #endif

        if 'v21town' in request_dict:
            v21town = request_dict['v21town']
            if v21town:
                voters = voters.filter(v21town=True)
            #endif
        #endif

        if 'v21primary' in request_dict:
            v21primary = request_dict['v21primary']
            if v21primary:
                voters = voters.filter(v21primary=True)
            #endif

        if 'v22general' in request_dict:
            v22general = request_dict['v22general']
            if v22general:
                voters = voters.filter(v22general=True)
            #endif
        #endif

        if 'v23town' in request_dict:
            v23town = request_dict['v23town']
            if v23town:
                voters = voters.filter(v23town=True)
            #endif
        #endif
        
        if 'voter_score' in request_dict:
            voter_score = request_dict['voter_score']
            if voter_score != "":
                voters = voters.filter(voter_score=int(voter_score))
            #endif
        #endif

        #date_of_birth__gte=int(min_year)
        if 'min_birth_year' in request_dict:
            min_birth_year = request_dict['min_birth_year']
            if min_birth_year and min_birth_year != "":
                voters = voters.filter(date_of_birth__gte=f"{min_birth_year}-01-01")
            #endif
        #endif

        if 'max_birth_year' in request_dict:
            max_birth_year = request_dict['max_birth_year']
            if max_birth_year and max_birth_year != "":
                voters = voters.filter(date_of_birth__lte=f"{max_birth_year}-12-31")
            #endif
            # print(f"Max birth year present? {max_birth_year}")
        #endif
        print(f"Number of results: {len(voters)}")
        # end of filtering logic 

        # start of graphing logic

        return voters
        #
    #enddef get _query set

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        voters = self.get_queryset()

        # dictionary of years
        birth_years = {k: 0 for k in range(1900,2025)}
        voter_scores = range(0,6)

        # order by date of birth
        # Voter.objects.filter(date_of_birth__gte="1990-01-01")
        for i in voters:
            # goes through every voter in already filtered voters list and adds them to their respective spot in the birth year dictionary
            birth_years[(i.date_of_birth).year] += 1
        #endfor
        fig = go.Bar(x=list(birth_years.keys()), y = list(birth_years.values()))
        title_text = f"Voters distribution by Year of Birth (n = {len(voters)})"
        bar_chart = plot({"data": [fig], 
                                         "layout_title_text": title_text,
                                         }, auto_open=False, output_type="div",               
                                         )
                                        
        context['bar_chart'] = bar_chart
        # end of bar chart logic

        # start of pie chart logic

        # end of pie chart logic 
        
        parties = Voter.objects.values_list('party_affiliation', flat=True).distinct().order_by('party_affiliation') 
        # for drop down
        party_affiliation_list = []

        for p in parties:
            if p: 
                party_affiliation_list.append(p) # in case of any whitespace
            #endif
        #endfor 

        context['party_affiliation'] = party_affiliation_list
        context['birth_years'] = range(1900, 2025)
        context['voter_score'] = range(0,6)
        return context
        # voters_by_birth = [v.]


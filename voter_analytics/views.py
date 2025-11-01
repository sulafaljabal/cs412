# voter_analytics/views.py
# Sulaf Al Jabal (U78815065) 10/31/25
# File description: views for voter_analytics application

from django.shortcuts import render

# Create your views here.
from django.db.models.query import QuerySet
from django.views.generic import ListView
from . models import *
 
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
        print(self.request.GET)
        if 'party_affiliation' in self.request.GET:
            party_affiliation = self.request.GET['party_affiliation']
            if party_affiliation and party_affiliation != "":
                voters = voters.filter(party_affiliation=party_affiliation.strip())
            #endif
        if 'v20state' in self.request.GET:
            v20state = self.request.GET['v20state']
            if v20state:
                voters = voters.filter(v20state=True)
            #endif

        if 'v21town' in self.request.GET:
            v21town = self.request.GET['v21town']
            if v21town:
                voters = voters.filter(v21town=True)
            #endif
        #endif

        if 'v21primary' in self.request.GET:
            v21primary = self.request.GET['v21primary']
            if v21primary:
                voters = voters.filter(v21primary=True)
            #endif

        if 'v22general' in self.request.GET:
            v22general = self.request.GET['v22general']
            if v22general:
                voters = voters.filter(v22general=True)
            #endif
        #endif

        if 'v23town' in self.request.GET:
            v23town = self.request.GET['v23town']
            if v23town:
                voters = voters.filter(v23town=True)
            #endif
        #endif
        
        if 'voter_score' in self.request.GET:
            voter_score = self.request.GET['voter_score']
            if voter_score != "":
                voters = voters.filter(voter_score=int(voter_score))
            #endif
        #endif
        return voters

        #date_of_birth__gte=int(min_year)
        if 'min_birth_year' in self.request.GET:
            min_birth_year = self.request.GET['min_birth_year']
            if min_birth_year != "":
                voters = voters.filter(date_of_birth__gte=int(min_birth_year))
            #endif
        #endif

        if 'max_birth_year' in self.request.GET:
            max_birth_year = self.request.GET['max_birth_year']
            if max_birth_year != "":
                voters = voters.filter(date_of_birth__lte=int(max_birth_year))
            #endif
            # print(f"Max birth year present? {max_birth_year}")
        #endif
        
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
        party_affiliation = []
        for p in parties:
            if p: 
                party_affiliation.append(p.strip()) # in case of any whitespace
            #endif
        #endfor 
        context['party_affiliation'] = party_affiliation
        context['birth_years'] = range(1900, 2025)
        context['voter_scores'] = range(0,6)
        return context
from yapsy.IPlugin import IPlugin
from yapsy.PluginManager import PluginManager
from django.template import loader, Context
from django.db.models import Count
from server.models import *
from django.shortcuts import get_object_or_404
import server.utils as utils

class SalScriptsVersion(IPlugin):
    def plugin_type(self):
        return 'builtin'
        
    def show_widget(self, page, machines=None, theid=None):
        # The data is data is pulled from the database and passed to a template.
        
        # There are three possible views we're going to be rendering to - front, bu_dashbaord and group_dashboard. If page is set to bu_dashboard, or group_dashboard, you will be passed a business_unit or machine_group id to use (mainly for linking to the right search).
        if page == 'front':
            t = loader.get_template('salscriptsversion/templates/front.html')
            if not machines:
                machines = Machine.objects.all()
        
        if page == 'bu_dashboard':
            t = loader.get_template('salscriptsversion/templates/id.html')
            if not machines:
                machines = utils.getBUmachines(theid)
        
        if page == 'group_dashboard':
            t = loader.get_template('salscriptsversion/templates/id.html')
            if not machines:
                machine_group = get_object_or_404(MachineGroup, pk=theid)
                machines = Machine.objects.filter(machine_group=machine_group)
        
        if machines:
            sal_info = machines.values('sal_version').exclude(sal_version__isnull=True).annotate(count=Count('sal_version')).order_by()
        else:
            sal_info = []

        c = Context({
            'title': 'Sal Version',
            'data': sal_info,
            'theid': theid,
            'page': page
        })
        return t.render(c), 4
    
    def filter_machines(self, machines, data):
        # You will be passed a QuerySet of machines, you then need to perform some filtering based on the 'data' part of the url from the show_widget output. Just return your filtered list of machines and the page title.
        
        machines = machines.filter(sal_version__exact=data)
        
        title = 'Machines running version '+data+' of Sal'
        return machines, title
        
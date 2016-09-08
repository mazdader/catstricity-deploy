# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.shortcuts import redirect
import os, time, subprocess
from ansible.inventory import Inventory
from ansible.parsing.dataloader import DataLoader
from ansible.vars import VariableManager
from django.conf import settings
from .models import Servers

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def loadAnsibleInventory():
    arr = {}
    loader = DataLoader()
    variable_manager = VariableManager()
    try:
        # Loading Ansible inventory
        inventory = Inventory(loader=loader, variable_manager=variable_manager,
                              host_list=settings.ANSIBLE_HOSTS_FILE)
        for group in inventory.list_groups():
            arr[str(group)] = []
        for host in inventory.list_hosts():
            for group in inventory.groups_for_host(str(host)):
                arr[str(group)].append(str(host))
        # Removing unneeded groups
        arr.pop('all', None)
        arr.pop('ungrouped', None)
    except:
        pass
    res = {}
    #Removing empty groups
    for key in arr:
        if len(arr[key]) <> 0:
            res[key] = arr[key]
    #Sorting items by length
    keys = sorted(res, key=lambda k: len(res[k]), reverse=True)
    return [res, keys]

def index(request):
    inventory = loadAnsibleInventory()
    #Removing in progress status for finished tasks
    for srv in Servers.objects.filter(server_status=True):
        if not os.path.isfile(os.path.join(os.path.join(BASE_DIR,'logs'), str(srv.server_id)) + ".inprogress"):
            srv.server_status = False
            srv.save()
    running_tasks = Servers.objects.filter(server_status=True)
    return render(request, 'app/index.html', {'host_list' : inventory[0], 'sorted_keys': inventory[1], 'running_tasks': running_tasks})

def runAnsible(request, server):
    server = os.path.basename(server)
    srv = Servers()
    #Running deployment task
    if server in [ item for sublist in loadAnsibleInventory()[0].values() for item in sublist] and not Servers.objects.filter(server_status=True, server_id=str(server)).exists():
        srv.server_id = str(server)
        srv.server_status = True
        srv.save()
        subprocess.Popen(['/bin/bash', '-c', '-x', "touch " + os.path.join(os.path.join(BASE_DIR,'logs'), str(server)) + ".inprogress ; "
                          + " rm " + os.path.join(os.path.join(BASE_DIR,'logs'), str(server)) + '.log' + " ; "
                          + " echo $(date) ; "
                          + " env ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook -D -v "
                          + " -i " + settings.ANSIBLE_HOSTS_FILE
                          + " --limit " + str(server)
                          + " --extra-vars='user=" + settings.ANSIBLE_USERNAME + "'"
                          + " --private-key " + settings.SSH_PRIVATE_KEY_PATH
                          + " " + os.path.join(os.path.join(BASE_DIR,'..'), "ansible/catstricity-deploy.yml")
                          + ' >>' + os.path.join(os.path.join(BASE_DIR,'logs'), str(server)+'.log')
                          + " 2>&1 && sleep 2s ; "
                          + " rm -f " + os.path.join(os.path.join(BASE_DIR,'logs'), str(server)) + ".inprogress ; " ],
                         stdout=subprocess.PIPE)
        #Just to be sure that file already created
        time.sleep(1)
    return redirect('view_results', server=server)

def viewResults(request, server):
    server = os.path.basename(server)
    logs = []
    if server in [ item for sublist in loadAnsibleInventory()[0].values() for item in sublist]:
        try:
            f = open(os.path.join(os.path.join(BASE_DIR,'logs'), str(server)+'.log'))
            for line in f:
                logs.append(line)
        except:
            logs.append("No previous deployments")
    else:
        logs.append("Error! Wrong server name...")
    return render(request, 'app/results.html', {'server': server, 'logs': logs})

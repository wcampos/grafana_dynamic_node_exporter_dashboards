# grafana_dynamic_node_exporter_dashboards
Create Dynamic Dashboards for Node Exporter / Prometheus Metrics

Running the generate_dashboards script, it will generate the dashboards under /var/lib/grafana/dashboards/mydash/ 

```bash
generate_dasboards.py
```

In order to import, use the grafana provisioning option by adding a file into */etc/grafana/provisioning/dashboards*

Here an example of the yaml file 

```bash 
apiVersion: 1

providers:
- name: 'mydash'
  orgId: 1
  folder: 'default' # Use any 
  folderUid: ''
  type: file
  disableDeletion: false
  editable: true
  updateIntervalSeconds: 300 # time to read changes on dashboards 
  allowUiUpdates: false
  options:
    path: /var/lib/grafana/dashboards/mydash
```

The first time you can restart grafana service 

```bash
systemctl restart grafana-server
```

Any other changes will take the time specified in *updateIntervalSeconds*

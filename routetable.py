###################################################################
#
# Sample script to update the route's next hop
#
###################################################################
import os
from azure.mgmt.resource import SubscriptionClient
from azure.identity import ClientSecretCredential
from azure.mgmt.network import NetworkManagementClient

##################################################################
# Retrieve the IDs and secret to use with ClientSecretCredential
# Parameters
subscription_id = os.environ["AZURE_SUBSCRIPTION_ID"]
tenant_id = os.environ["AZURE_TENANT_ID"]
client_id = os.environ["AZURE_CLIENT_ID"]
client_secret = os.environ["AZURE_CLIENT_SECRET"]
resource_group = "dchaocrossaz"
next_hop = "1.1.1.1"
route_name = "10.0.0.0"
route_table_name = "internal-route"



##################################################################
#
credential = ClientSecretCredential(tenant_id=tenant_id, client_id=client_id, client_secret=client_secret)

network_client = NetworkManagementClient(credential, subscription_id=subscription_id)

#route_table_list = network_client.route_tables.list_all()
route_table_list = network_client.route_tables.list(resource_group_name=resource_group)

for route_table in route_table_list:
    route_list = network_client.routes.list(resource_group_name=resource_group, route_table_name=route_table.name)
    for route in route_list:
        if route_table.name == route_table_name:
            print ("Route Table Name: ", route_table.name, "Route Name: " , route.name)
            route = network_client.routes.get(resource_group_name=resource_group, route_table_name=route_table.name, route_name=route.name)
            if route.next_hop_type == "VirtualAppliance":
                if route.name == route_name:
                    print ("Before: ", route)
                    route_prefix = route.address_prefix
                    rg_result = network_client.routes.begin_create_or_update(resource_group_name=resource_group, route_table_name=route_table.name, route_name=route.name, route_parameters=
                            {
                                "address_prefix" : route_prefix,
                                "next_hop_type" : "VirtualAppliance",
                                "next_hop_ip_address": next_hop
                            }
                        )
                    print ("Result: " , rg_result.result())

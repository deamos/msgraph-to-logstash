from lib import MSGraph
from lib import filters
from lib import logstash

import datetime

ls = logstash.logstash("logstash.example.com", 5000)

tenant = "tenant_id_here"
client_id = "client_id_here"
client_secret = "client_secret_here"

graph_obj = MSGraph.graph(tenant, client_id, client_secret)
graph_obj.getClientAccessToken()


endpoint = "https://graph.microsoft.com/v1.0/auditLogs/signIns"
startTime = datetime.datetime.utcnow() - datetime.timedelta(minutes=10)
startTimeStr = startTime.isoformat(' ', 'seconds').replace(' ','T') + "Z"
params = {
    "$filter": "createdDateTime ge " + startTimeStr
}

data = MSGraph.getEndpointData(token, endpoint, params)
for entry in data['value']:
    entry['type'] = "AAD_Sign_In"
    flattenedJSON = filters.flatten_json(entry)
    ls.sendmsg(flattenedJSON)

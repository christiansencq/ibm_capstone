#
#
# main() will be run when you invoke this action
#
# @param Cloud Functions actions accept a single parameter, which must be a JSON object.
#
# @return The output of this action, which must be a JSON object.
#
#
from cloudant.client import Cloudant
from cloudant.error import CloudantException
import requests


def main(dict):



        # client=Cloudant(
        #     dict["COUCH_USERNAME"],
        #     dict["ZHDaKveTQOV3dbrrx2lx17uGCXXFbw8kAU0CA5hEZ7IT"],
        #     url=dict["https://apikey-v2-ex50zt74fdon5ojl817z8oh0t9p2ksi4j7shgcpqhb0:88d46706d5b61082f03e097985284b9c@b8313b34-4a62-4bbc-912e-c754459259ca-bluemix.cloudantnosqldb.appdomain.cloud"],
        #     connect=True,
        # )
    databaseName = "reviews"
    try:
        account_user_name = "apikey-v2-ex50zt74fdon5ojl817z8oh0t9p2ksi4j7shgcpqhb0"
        apikey = "ZHDaKveTQOV3dbrrx2lx17uGCXXFbw8kAU0CA5hEZ7IT"
        url = "https://apikey-v2-ex50zt74fdon5ojl817z8oh0t9p2ksi4j7shgcpqhb0:88d46706d5b61082f03e097985284b9c@b8313b34-4a62-4bbc-912e-c754459259ca-bluemix.cloudantnosqldb.appdomain.cloud"
        client = Cloudant.iam(
            account_name=account_user_name,
            api_key=apikey,
            connect=True,
        )
        print("Databases: {0}".format(client.all_dbs()))
    except CloudantException as ce:
        print("unable to connect")
        return {"error": ce}
    except (requests.exceptions.RequestException, ConnectionResetError) as err:
        print("connection error")
        return {"error": err}
    print("Success")
    return {"dbs": client.all_dbs()}

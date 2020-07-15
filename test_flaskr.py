import os
import unittest
import requests
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, ServiceRequest

class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client

        self.database_user = 'postgres'
        self.database_password = 'Murakami20'
        self.database_host = 'localhost:5432'
        self.database_name = "servicebroker_test"
        self.database_path = "postgres://{}:{}@{}/{}".format(self.database_user, self.database_password, self.database_host, self.database_name)

        self.admin_token_no_auth = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c'
        self.admin_token_expired = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlNaYmhmV0pkaGpqZ2R3clFqR1l0aCJ9.eyJpc3MiOiJodHRwczovL3VkYWNpdHktZnNuZC5ldS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWYwMWFiODc3NjAwNDQwMDEzOTlmMWYxIiwiYXVkIjoic2VydmljZXJlcXVlc3QiLCJpYXQiOjE1OTQzNzg3NTUsImV4cCI6MTU5NDQ2NTE1NSwiYXpwIjoiTUVZdU1jMEtlYUNQWll5MXlJdElFMDZIS2htTmV2YTkiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTpzZXJ2aWNlcmVxdWVzdCIsImdldDpob3NwaXRhbHMiLCJnZXQ6c2VydmljZXJlcXVlc3RzIiwicGF0Y2g6c2VydmljZXJlcXVlc3QiLCJwb3N0OnNlcnZpY2VyZXF1ZXN0Il19.De2ykyMFxoUrPSLqs_AgnAoiuR7dOgFwLmunS6tLs6LGIies2ZTJKovv-EHJpL0R2sx54U-O0IXSuAYIN63Zjinl13S6dBmF1xDgGHhPZKSd96Np4AxPklNGzw3jCjD3I7TbGoXGuYF6TTZNwGR3M6OYL5PBHVc5O-gpt78IbAmVTHmWpqTXdP6oc4d_mb4Pn5yRlnALc1LmzXT7u0y7NhOyk8Q5V6PptEZSevdP9K4yr1Oiwteoiy4lRAe-b0cMATiM18x3GyZkaKAFBXIWNUFCfp-4ZYlMXlxJ_9quU1PhbpXjeXV70CTcCF_AkY-uSH31AJT5dbi25XnWKnXA6A'
        self.admin_token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlNaYmhmV0pkaGpqZ2R3clFqR1l0aCJ9.eyJpc3MiOiJodHRwczovL3VkYWNpdHktZnNuZC5ldS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWYwMWFiODc3NjAwNDQwMDEzOTlmMWYxIiwiYXVkIjoic2VydmljZXJlcXVlc3QiLCJpYXQiOjE1OTQ3MTg0NTUsImV4cCI6MTU5NDgwNDg1NSwiYXpwIjoiTUVZdU1jMEtlYUNQWll5MXlJdElFMDZIS2htTmV2YTkiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTpzZXJ2aWNlcmVxdWVzdCIsImdldDpob3NwaXRhbHMiLCJnZXQ6c2VydmljZXJlcXVlc3RzIiwicGF0Y2g6c2VydmljZXJlcXVlc3QiLCJwb3N0OnNlcnZpY2VyZXF1ZXN0Il19.vfPzFLFzyNogULYG1thRSiFc1A3SQ1VXImVRdgOA8rqncee19RWZcxbRsoq4bz3PvN7ZUB7e1s894N3iIYQtvOAieGbd_-SoZrtOB9gt98Ci8GqbOEXNAQ_G4oO-QVxzE8KMhreuU4nuUmQmYi0Vb-WzDJdL5Rv79T13ck0I_fO7teedwS3bZa-QN7D_Nsl9IJg3a-a3aSVSm11B7U9pVxGgNDvMCaMZpcv75KNZPOae7KvTGbQyY7zyb7XJ47bz1GTjF11ihnDhXNr3qJClgMmHbMNahvBEilHQlfH3rt1TCN1xPz4GV2ajrO51dFlo0fUgTWnoaohpOEZi28lo1A'
        self.client_token_no_auth = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c'
        self.client_token_expired = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlNaYmhmV0pkaGpqZ2R3clFqR1l0aCJ9.eyJpc3MiOiJodHRwczovL3VkYWNpdHktZnNuZC5ldS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWYwNmUwYjU2YjI1NjEwMDE5MTNkMjAwIiwiYXVkIjoic2VydmljZXJlcXVlc3QiLCJpYXQiOjE1OTQ2MjY1ODcsImV4cCI6MTU5NDcxMjk4NywiYXpwIjoiTUVZdU1jMEtlYUNQWll5MXlJdElFMDZIS2htTmV2YTkiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImdldDpob3NwaXRhbHMiLCJwb3N0OnNlcnZpY2VyZXF1ZXN0Il19.SUfgLq1mmwdS7kuHzBV1_sxV9mCe1IpO0IHVLBqsmv67HuxKBTeqJ2WPVzGLDgAwuukwlNFPYSYcUzslUzwQH4tzHrQCpTrKUWAu1A59RW1w1n2Zrul9W2D14-B8PyTfjY_qusDRjC57YfOOWt0Q9pGXy8D_r4zjGsOxAMjJewncaBqwqrGO1lyKGrGUe8IxabNUS7gtc5AgSHtmsiVWXcw1lQgDogHV9Paf8zKaRfuHOglqK7KjgzcFyU1JMndOwhReGjTx9I9Vpw83GBMbIiCRbhACMgUTgboJ2aBpw2SFQoj3fV1lhw3eXjFMg1nieecppGFOXzCW6rQc35bzNA'
        self.client_token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlNaYmhmV0pkaGpqZ2R3clFqR1l0aCJ9.eyJpc3MiOiJodHRwczovL3VkYWNpdHktZnNuZC5ldS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWYwNmUwYjU2YjI1NjEwMDE5MTNkMjAwIiwiYXVkIjoic2VydmljZXJlcXVlc3QiLCJpYXQiOjE1OTQ3MTg1NzAsImV4cCI6MTU5NDgwNDk3MCwiYXpwIjoiTUVZdU1jMEtlYUNQWll5MXlJdElFMDZIS2htTmV2YTkiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImdldDpob3NwaXRhbHMiLCJwb3N0OnNlcnZpY2VyZXF1ZXN0Il19.GxQrhE2_OlnPBCOqGf2lvezZC9BHuksoLANk6ohnWII09ANrN6zcv8jf7KA0yT9ATIokzs_ME_DK11w-5oqOZ3zAnp8vELF29huzGscP-bDRjKLxj9kCCtBIcACmogTmSNe8YEi-FQZEvSTcN-uIoBrlFZH_H2eRNJyVtMmhOrh8KEUfg4pQlS78YRPonmszNhZALdhW_CBGy1GSWq6kzeoG7DQ1sCk87mr-Ko0w1uIP82VyBBySlzb8rmg5qY-e_nzMq8TlDxtFkd2xn7lwxVM2ZiJRfwRM0R8yDSIM5VDaCfLbd91603N8zOAWIHqTY2M6DE8RBQx2fu_5X4jssA'


        setup_db(self.app, self.database_path)

        self.new_servicerequest = {
            "origin_airport": "Universitaetsklinik Innsbruck",
            "destination_airport": "Klinikum Grosshadern",
            "payload": "Kidney",
            "payload_weight": "5",
            "priority": True,
            "status": "Requested",
            "collection_datetime": "2020-05-28 11:30:00",
            "delivery_datetime": "2020-05-28 12:30:00",
            "latest_delivery_datetime": "2020-05-28 13:30:00"
        }

        self.new_servicerequest_accepted = {
            "origin_airport": "Universitaetsklinik Innsbruck",
            "destination_airport": "Klinikum Grosshadern",
            "payload": "Kidney",
            "payload_weight": "5",
            "priority": True,
            "status": "Scheduled",
            "collection_datetime": "2020-05-28 11:30:00",
            "delivery_datetime": "2020-05-28 12:30:00",
            "latest_delivery_datetime": "2020-05-28 13:30:00"
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    # GET servicerequests endpoint

    def test_a_get_servicerequests_admin(self):

        res = self.client().get('/servicerequests', 
        headers={"Authorization": "Bearer {}".format(self.admin_token)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        # self.assertTrue(data['requests'])
        # self.assertEqual(len(data['requests']), 0)

    def test_b_get_servicerequests_client(self):

        res = self.client().get('/servicerequests', 
        headers={"Authorization": "Bearer {}".format(self.client_token)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Permission not found.')

    # POST servicerequest endpoint

    def test_c_create_servicerequest(self):
        res = self.client().post('/servicerequests', data=json.dumps(self.new_servicerequest), 
        headers={'Content-Type': 'application/json', 
        "Authorization": "Bearer {}".format(self.admin_token)})
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])
        self.assertTrue(data['total_servicerequests'])

    def test_d_create_servicerequest_no_auth_header(self):
        res = self.client().post('/servicerequests', 
        data=json.dumps(self.new_servicerequest), 
        headers={'Content-Type': 'application/json'})
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Authorization header is expected.')
    
    # PATCH servicerequest endpoint

    def test_e_update_servicerequest(self):
        res = self.client().patch('/servicerequests/1', 
        data=json.dumps(self.new_servicerequest_accepted), 
        headers={'Content-Type': 'application/json', 
        "Authorization": "Bearer {}".format(self.admin_token)})
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['updated_servicerequest_id'], 1)
        self.assertEqual(data['status'], 'Scheduled')

    def test_f_update_servicerequest_auth_error(self):
        res = self.client().patch('/servicerequests/1',  
        data=json.dumps(self.new_servicerequest_accepted), 
        headers={'Content-Type': 'application/json', 
        "Authorization": "Bearer {}".format(self.client_token)})
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Permission not found.')

    # DELETE servicerequest endpoint

    def test_g_404_if_servicerequest_does_not_exist(self):
        res = self.client().delete('/servicerequests/1000', 
        headers={'Content-Type': 'application/json', 
        "Authorization": "Bearer {}".format(self.admin_token)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable.')

    def test_h_delete_servicerequest(self):
        res = self.client().delete('/servicerequests/1', 
        headers={'Content-Type': 'application/json', 
        "Authorization": "Bearer {}".format(self.admin_token)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    # GET hospitals endpoint

    def test_i_get_hospitals_client(self):

        res = self.client().get('/hospitals', 
        headers={"Authorization": "Bearer {}".format(self.client_token)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['hospitals'])
        self.assertEqual(len(data['hospitals']), 2)

    def test_j_get_hospitals_auth_error(self):

        res = self.client().get('/hospitals')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    # Further RBAC tests

    def test_k_get_servicerequests_admin_expired_token(self):

        res = self.client().get('/servicerequests', 
        headers={"Authorization": "Bearer {}".format(self.admin_token_expired)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Token expired.')

    def test_l_get_servicerequests_admin_no_auth_token(self):

        res = self.client().get('/servicerequests', 
        headers={"Authorization": "Bearer {}".format(self.admin_token_no_auth)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Authorization malformed.')

    def test_m_get_servicerequests_client_expired_token(self):

        res = self.client().get('/servicerequests', 
        headers={"Authorization": "Bearer {}".format(self.client_token_expired)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Token expired.')

    def test_n_get_servicerequests_client_no_auth_token(self):

        res = self.client().get('/servicerequests', 
        headers={"Authorization": "Bearer {}".format(self.client_token_no_auth)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Authorization malformed.')

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()

  # dropdb -U postgres servicebroker
  # createdb -U postgres servicebroker
  # psql -U postgres servicebroker < servicebroker.psql
  # psql -d servicebroker -U postgres -a -f servicebroker.psql
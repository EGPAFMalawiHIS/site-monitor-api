from rest_framework.test import APITestCase
from rombot.models import (
    User, Genders, Languages, Countries, Institutions,
    Joints, Descriptions, VerificationCodeTypes, Roles,
    Exercises, Locales, PartOfDay, QuestionTypes,)


class SimpleModelsTestCase(APITestCase):
    def setUp(self):
        self.username = 'john_doe'
        self.password = 'foobar'
        self.user = User.objects.create(
                        username=self.username, password=self.password)
        self.user.active = True
        self.client.force_authenticate(user=self.user)

    def test_create_simple_models(self):
        '''structure = {'model1': {'url': 'testurl',
                                   'params': {'param1': 1,
                                              'param2': 2,
                                              },
                                   },
                        'model2': {'url': 'testurl2',
                                    'params':{'params3': 3,
                                              'params4': 4}}
                        etc,
                     }
        '''
        structure = {}
        models = [Genders, Languages, Countries, Institutions, Joints,
                  Descriptions, VerificationCodeTypes, Roles, Exercises,
                  Locales, PartOfDay, QuestionTypes, ]

        for model in models:
            model_name = model._meta.db_table
            model_fields = model._meta.get_fields()
            # TODO: Do datefields aswell
            param_keys = filter(
                            lambda i: i.get_internal_type() == 'CharField'
                            or i.get_internal_type() == 'IntegerField',
                            model_fields)
            # param_keys is list of tuples
            # [(fieldname, internaly_type),
            #  (fieldname, internaly_type),
            # ]
            param_keys = [(p.name, p.get_internal_type()) for p in param_keys]
            # field and value pair
            # param_keys_values -  values strings and integers field types
            # d = {n: n**2 for n in range(5)}
            # print d
            # {0: 0, 1: 1, 2: 4, 3: 9, 4: 16}
            param_keys_values = {
                                n: '{}'.format(m) == 'IntegerField'
                                and 1
                                or '{}-1'.format(n) for n, m in param_keys}

            if model_name == 'locales':  # length < 5
                param_keys_values = {'locale_key': 'key-1'}
            structure[model_name] = {'url': '/api/{}/'.format(model_name),
                                     'params': param_keys_values}

        for st in structure:
            response = self.client.post(
                            structure[st]['url'], structure[st]['params'],
                            format='json')
            self.assertEqual(response.status_code, 201)

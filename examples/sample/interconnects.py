from hpOneView.resources.networking.interconnects import Interconnects
from pprint import pprint
from hpOneView.connection import connection

credential = dict(
    userName='Administrator',
    password='password'
)
one_view_connection = connection('127.0.0.1')
one_view_connection.login(credential)

interconnects_id = 'ad28cf21-8b15-4f92-bdcf-51cb2042db32'
interconnect = Interconnects(one_view_connection)
statistics = interconnect.get_interconnects_statistics(interconnects_id)
pprint(statistics)

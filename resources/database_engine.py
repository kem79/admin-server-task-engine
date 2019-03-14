#
# from sqlalchemy import create_engine
#
#
# class DatabaseEngineSingleton:
#
#     __engine = None
#
#     @staticmethod
#     def get_instance():
#         if not DatabaseEngineSingleton.__engine:
#             DatabaseEngineSingleton()
#         return DatabaseEngineSingleton.__engine
#
#     def __init__(self):
#         if DatabaseEngineSingleton.__engine:
#             raise Exception('This is a singleton class')
#         else:
#             self.__engine = create_engine('postgres://guest:guest@192.168.99.100:5432/guest')
#             self.metadata = MetaData
#             self.table = Table('applications', self.metadata,
#                        Column('id', Integer(), autoincrement="auto", primary_key=True, index=True),
#                        Column('name', String(), unique=True))
#             DatabaseEngineSingleton.__engine = self
#
#
#
#
#
#

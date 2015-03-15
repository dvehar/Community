from gluon.tools import Auth
db = DAL("sqlite://storage.sqlite")
auth = Auth(db)


# member table (used for auth)
db.define_table(
    auth.settings.table_user_name,
    Field('first_name', length=128, default=''),
    Field('last_name', length=128, default=''),
    Field('primary_address', length=128, default=''),
    Field('email', length=128, default='', unique=True), # required
    Field('password', 'password', length=512, readable=False, label='Password'), # required
    Field('registration_key', length=512,                # required
          writable=False, readable=False, default=''),
    Field('reset_password_key', length=512,              # required
          writable=False, readable=False, default=''),
    Field('registration_id', length=512,                 # required
          writable=False, readable=False, default=''))

custom_auth_table = db[auth.settings.table_user_name] # get the custom_auth_table

custom_auth_table.email.requires = IS_EMPTY_OR(IS_EMAIL())
custom_auth_table.password.requires = [CRYPT()]

auth.settings.table_user = custom_auth_table # tell auth to use custom_auth_table

auth.define_tables(username=False, signature=False)


#the community
db.define_table('community',
   Field('title', 'string', unique=True),
   Field('public_description', 'string'),
   Field('private_description', 'string'),
   Field('searchable', 'boolean')
)

#the members of a community
db.define_table('community_members',
   Field('member_id', 'reference auth_user'),
   Field('community_id', 'reference community'),
)

#the description of a community member
db.define_table('member_description',
   Field('member_id', 'reference auth_user'),
   Field('community_id', 'reference community'),
   Field('description', 'string')
)

#the contact info of a community member
db.define_table('member_contact_info',
   Field('member_id', 'reference auth_user'),
   Field('community_id', 'reference community'),
   Field('info', 'string'),
   Field('info_type', 'string')
)

#the people related to a community member
db.define_table('member_relationship',
   Field('member_id', 'reference auth_user'),
   Field('community_id', 'reference community'),
   Field('name', 'reference auth_user'),
   Field('relationship_description', 'string')
)

#todo required / optional

# todo writeable / readables
# db.post.image_id.writable = db.post.image_id.readable = False
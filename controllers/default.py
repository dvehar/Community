# -*- coding: utf-8 -*-

@auth.requires_login()
def index():
    first_name = auth.user.first_name
    last_name = auth.user.last_name
    communities = db(auth.user.id == db.community_members.member_id).select(db.community_members.community_id)
    community_names_ids = []
    for x in range(len(communities)):
      #print str(x) + "--" + str(communities[x].community_id)
      community_names_ids.append(( (db(db.community.id == communities[x].community_id).select(db.community.title).first().title) , (communities[x].community_id)) )
    return dict(first_name=first_name, last_name=last_name, community_names_ids=community_names_ids)

@auth.requires_login()
def create_community():
    form = SQLFORM(db.community)
    if form.process().accepted:
      db.community_members.insert(member_id=auth.user.id, community_id=db().select(db.community.id).last())
      session.flash = 'Community \'' + form.vars.title + '\' created.'
      redirect(URL('default', 'index'))
    return dict(form=form)
    
### request.args(0) the id of the community ###
@auth.requires_login()
def view_community():
    community_info = db(db.community.id == request.args(0)).select().first()
    if (community_info == None):
      session.flash = 'Invalid community ID'
      redirect(URL('default', 'index'))
    return dict(community_info=community_info)
    

def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/manage_users (requires membership in
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


@auth.requires_login() 
def api():
    """
    this is example of API with access control
    WEB2PY provides Hypermedia API (Collection+JSON) Experimental
    """
    from gluon.contrib.hypermedia import Collection
    rules = {
        '<tablename>': {'GET':{},'POST':{},'PUT':{},'DELETE':{}},
        }
    return Collection(db).process(request,response,rules)

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 21 15:14:59 2020

@author: Sam Terfa
"""

from google.oauth2 import service_account
import googleapiclient.discovery
import json
import pandas as pd
import numpy as np
import os

# This function checks the presence of necessary environmental variables before making API requests.
def check_credentials(module, scopes):

    """
    Check Google credentials for the user

    Args:
        module: which Google API to check credentials for
        
        scopes: the requested scopes for the API
    """    

    try:
        os.environ[module + '_service_account_file_path']
    except:
        raise Exception('os.environ[' + module + '_service_account_file_path"] must be set! This is the path to your service account json file.')

    try:
        os.environ[module + "_google_user"]
    except:
        raise Exception('os.environ[' + module + '_google_user] must be set! This is the email address of the user making requests.')

    credentials = service_account.Credentials.from_service_account_file(os.environ[module + "_service_account_file_path"], scopes = scopes, subject=os.environ[module + "_google_user"])
    
    credentials.admin_directory = googleapiclient.discovery.build('admin', 'directory_v1', credentials=credentials)
    
    return credentials

#### MEMBERS http://googleapis.github.io/google-api-python-client/docs/dyn/admin_directory_v1.members.html

module = 'admin_directory'
scopes = ['https://www.googleapis.com/auth/admin.directory.group']
admin_directory_credentials = check_credentials(module = module, scopes = scopes)

def removeGoogleGroupMember(groupKey, memberKey):
    
    """
    Remove membership.

    Args:
        groupKey: string, Email or immutable ID of the group (required)
        
        memberKey: string, Email or immutable ID of the member (required)
        
    More Info:
        https://developers.google.com/admin-sdk/directory/v1/reference
    """
    
    req = admin_directory_credentials.admin_directory.members().delete(groupKey = groupKey, memberKey = memberKey)
    
    results = req.execute()
    
    return(memberKey + ' successfully removed from ' + groupKey)

def getGoogleGroupMember(groupKey, memberKey):
    
    """
    
    Retrieve Group Member

    Args:
      groupKey: string, Email or immutable ID of the group (required)
      
      memberKey: string, Email or immutable ID of the member (required)
    
    Returns:
      An object of the form:
    
        { # JSON template for Member resource in Directory API.
          "status": "A String", # Status of member (Immutable)
          "kind": "admin#directory#member", # Kind of resource this is.
          "delivery_settings": "A String", # Delivery settings of member
          "id": "A String", # Unique identifier of customer member (Read-only) Unique identifier of group (Read-only) Unique identifier of member (Read-only)
          "etag": "A String", # ETag of the resource.
          "role": "A String", # Role of member
          "type": "A String", # Type of member (Immutable)
          "email": "A String", # Email of member (Read-only)
        }
    
    """
    
    req = admin_directory_credentials.admin_directory.members().get(groupKey = groupKey, memberKey = memberKey)
    
    results = req.execute()
    
    member = pd.DataFrame([list(results.values())], columns = results.keys())
    
    return(member)

def getGoogleGroupMemberExists(groupKey, memberKey):
    
    """
    
    Checks whether the given user is a member of the group. Membership can be direct or nested.

    Args:
      groupKey: string, Identifies the group in the API request. The value can be the group's email address, group alias, or the unique group ID. (required)
      
      memberKey: string, Identifies the user member in the API request. The value can be the user's primary email address, alias, or unique ID. (required)
    
    Returns:
      An object of the form:
    
        { # JSON template for Has Member response in Directory API.
        "isMember": True or False, # Identifies whether the given user is a member of the group. Membership can be direct or nested.
      }
        
    """
    
    req = admin_directory_credentials.admin_directory.members().hasMember(groupKey = groupEmail, memberKey = memberEmail)
    
    results = req.execute()
    
    return(results['isMember'])

def createGoogleGroupMember(groupKey, member_email, member_role, member_delivery_settings = None, member_etag = None):

    """    
    Add user to the specified group.
    
    Args:
      groupKey: string, Email or immutable ID of the group (required)
      
      body: object, The request body. (required)
      
        The object takes the form of:
    
    { # JSON template for Member resource in Directory API.
        "status": "A String", # Status of member (Immutable)
        "kind": "admin#directory#member", # Kind of resource this is.
        "delivery_settings": "A String", # Delivery settings of member
        "id": "A String", # Unique identifier of customer member (Read-only) Unique identifier of group (Read-only) Unique identifier of member (Read-only)
        "etag": "A String", # ETag of the resource.
        "role": "A String", # Role of member
        "type": "A String", # Type of member (Immutable)
        "email": "A String", # Email of member (Read-only)
      }
    
    Returns:
      An object of the form:
    
        { # JSON template for Member resource in Directory API.
          "status": "A String", # Status of member (Immutable)
          "kind": "admin#directory#member", # Kind of resource this is.
          "delivery_settings": "A String", # Delivery settings of member
          "id": "A String", # Unique identifier of customer member (Read-only) Unique identifier of group (Read-only) Unique identifier of member (Read-only)
          "etag": "A String", # ETag of the resource.
          "role": "A String", # Role of member
          "type": "A String", # Type of member (Immutable)
          "email": "A String", # Email of member (Read-only)
        }
        return(newMember)

    """
    
    params = pd.DataFrame(list(zip(locals().keys(), locals().values())), columns = ["Param", "Value"]).query('Param.str.startswith("member_") and Value.notnull()')
    
    params.Param = params.Param.str.replace('member_', '')
    
    body = dict()
    for i in range(0, len(params.Param)-1):
        
        body[list(params.Param)[i]] = list(params.Value)[i]
    
    results = admin_directory_credentials.admin_directory.members().insert(groupKey = groupKey, body = body).execute()
    
    member = pd.DataFrame([list(results.values())], columns = results.keys())
    
    return(member)


def listGoogleGroupMembers(groupKey, pageToken=None, maxResults=None, roles=None, includeDerivedMembership=None):
    
    """
    
    Retrieve all members in a group (paginated)

    Args:
      groupKey: string, Email or immutable ID of the group (required)
      
      pageToken: string, Token to specify next page in the list
      
      maxResults: integer, Maximum number of results to return. Default is 200
      
      roles: string, Comma separated role values to filter list results on.
      
      includeDerivedMembership: boolean, Whether to list indirect memberships. Default: false.
    
    Returns:
      An object of the form:
    
        { # JSON response template for List Members operation in Directory API.
        "nextPageToken": "A String", # Token used to access next page of this result.
        "kind": "admin#directory#members", # Kind of resource this is.
        "etag": "A String", # ETag of the resource.
        "members": [ # List of member objects.
          { # JSON template for Member resource in Directory API.
              "status": "A String", # Status of member (Immutable)
              "kind": "admin#directory#member", # Kind of resource this is.
              "delivery_settings": "A String", # Delivery settings of member
              "id": "A String", # Unique identifier of customer member (Read-only) Unique identifier of group (Read-only) Unique identifier of member (Read-only)
              "etag": "A String", # ETag of the resource.
              "role": "A String", # Role of member
              "type": "A String", # Type of member (Immutable)
              "email": "A String", # Email of member (Read-only)
            },
        ],
      }
    
    """
    
    req = admin_directory_credentials.admin_directory.members().list(groupKey = groupKey, pageToken=pageToken, maxResults=maxResults, roles=roles, includeDerivedMembership=includeDerivedMembership)
    
    results = req.execute()
    
    members = pd.DataFrame(results['members'])
    
    while 'nextPageToken' in results.keys():
    
        pageToken = results['nextPageToken']
    
        req = admin_directory_credentials.admin_directory.members().list(groupKey = groupKey, pageToken=pageToken, maxResults=maxResults, roles=roles, includeDerivedMembership=includeDerivedMembership)
    
        results = req.execute()
        
        members = pd.concat([members, pd.DataFrame(results['members'])])
    
    return members


def updateGoogleGroupMember(groupKey, memberKey, member_role, member_delivery_settings = None, member_etag = None):
    
    """
    Update membership of a user in the specified group. This method supports patch semantics.

    Args:
      groupKey: string, Email or immutable ID of the group. If ID, it should match with id of group object (required)
      
      memberKey: string, Email or immutable ID of the user. If ID, it should match with id of member object (required)
      
      body: object, The request body. (required)
      
        The object takes the form of:
    
    { # JSON template for Member resource in Directory API.
        "status": "A String", # Status of member (Immutable)
        "kind": "admin#directory#member", # Kind of resource this is.
        "delivery_settings": "A String", # Delivery settings of member
        "id": "A String", # Unique identifier of customer member (Read-only) Unique identifier of group (Read-only) Unique identifier of member (Read-only)
        "etag": "A String", # ETag of the resource.
        "role": "A String", # Role of member
        "type": "A String", # Type of member (Immutable)
        "email": "A String", # Email of member (Read-only)
      }
    
    
    Returns:
      An object of the form:
    
        { # JSON template for Member resource in Directory API.
          "status": "A String", # Status of member (Immutable)
          "kind": "admin#directory#member", # Kind of resource this is.
          "delivery_settings": "A String", # Delivery settings of member
          "id": "A String", # Unique identifier of customer member (Read-only) Unique identifier of group (Read-only) Unique identifier of member (Read-only)
          "etag": "A String", # ETag of the resource.
          "role": "A String", # Role of member
          "type": "A String", # Type of member (Immutable)
          "email": "A String", # Email of member (Read-only)
        }
    """
    
    params = pd.DataFrame(list(zip(locals().keys(), locals().values())), columns = ["Param", "Value"]).query('Param.str.startswith("member_") and Value.notnull()')
    
    params.Param = params.Param.str.replace('member_', '')
    
    body = dict()
    for i in range(0, len(params.Param)-1):
        
        body[list(params.Param)[i]] = list(params.Value)[i]
    
    req = admin_directory_credentials.admin_directory.members().patch(groupKey = groupKey, memberKey = memberKey, body = body)
    
    results = req.execute()
    
    member = pd.DataFrame([list(results.values())], columns = results.keys())
    
    return(member)
    
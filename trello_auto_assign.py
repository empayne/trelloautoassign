#!/usr/bin/env python

# TrelloAutoAssign
# Takes a user's boards under a given team/organization name, and assigns all of
# them to that user. Intended for personal use. We want this because Trello does
# not support automatically assigning new cards to a given user, and we want to
# be able to see all of our cards we've created in list of due date under our
# assigned cards view.

import os
from trello import TrelloApi

def main():
    print 'Starting execution of TrelloAutoAssign.'

    TRELLO_USERNAME = os.environ['TRELLO_USERNAME']
    # Autoassign cards with this team name. Necessary because Trello has no
    # 'handshake' when adding another user to a board,and the API doesn't
    # expose the board's creator. We don't want to reassign every card in every
    # board we're added to.
    TRELLO_AA_ORGANIZATION_NAME = os.environ['TRELLO_AA_ORGANIZATION_NAME']
    # Unassign items that are finished so that they don't show up in our
    # assigned cards view anymore.
    UNASSIGN_LIST_NAME = 'Done'
    # App key from: https://trello.com/app-key
    # Token from: trello.get_token_url('TrelloAutoAssign', expires='never', write_access=True)
    TRELLO_APP_KEY = os.environ['TRELLO_APP_KEY']
    TRELLO_TOKEN = os.environ['TRELLO_TOKEN']
    trello = TrelloApi(TRELLO_APP_KEY)
    trello.set_token(TRELLO_TOKEN)

    user = trello.members.get(TRELLO_USERNAME)
    user_id = user['id']
    list_names = {}
    total_assignments = 0

    board_ids = user['idBoards']
    for board_id in board_ids:
        board = trello.boards.get(board_id)
        if not board['closed'] and board['idOrganization'] is not None:
                organization = trello.organizations.get(board['idOrganization'])
                if organization['name'] == TRELLO_AA_ORGANIZATION_NAME:
                    # Trello batch GET request unsupported in Python library :(
                    cards = trello.boards.get_card(board_id)
                    for card in cards:
                        assigned = assign(trello, user_id, card, list_names, UNASSIGN_LIST_NAME)
                        if assigned:
                            print 'Changed assignment of: ' + card['name']
                            total_assignments = total_assignments + 1

    print 'Finished execution. Changed assignments of ' + str(total_assignments) + ' total cards.'

def assign(trello, user_id, card, list_names, UNASSIGN_LIST_NAME):
    assigned = False
    card_done = is_list_done(trello, card['idList'], list_names, UNASSIGN_LIST_NAME)
    if card_done and card['idMembers'] != []:
            trello.cards.delete_member_idMember(user_id, card['id'])
            assigned = True
    elif (not card_done) and card['idMembers'] == []:
        trello.cards.new_member(card['id'], user_id)
        assigned = True
    return assigned

def is_list_done(trello, idList, list_names, UNASSIGN_LIST_NAME):
    # Effectively cache our result. Problems if list name changes while running.
    if not idList in list_names:
        list = trello.lists.get(idList)
        list_names[idList] = list['name']
    return list_names[idList] == UNASSIGN_LIST_NAME

main()

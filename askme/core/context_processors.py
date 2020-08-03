def active_user_board_url(request):
    return {
        'BOARD_URL': request.build_absolute_uri(f'/board/{request.user.username}') 
    }
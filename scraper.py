import time
import sys

from app.main_app import MainApp
from app.parse_engine import ParseEngine


def main():
    # Update url here or pass it as a parameter
    url = "https://statsapi.mlb.com/api/v1.1/game/644006/feed/live"

    if len(sys.argv) == 1:
        url = sys.argv[0]

    parser: ParseEngine = ParseEngine(1)
    display: MainApp = MainApp()

    print("start")
    parser.start()

    time.sleep(20)

    print("stop")
    parser.stop()


    # with urllib.request.urlopen(url) as url_data:
    #     data = json.loads(url_data.read().decode())
    #
    #     config = {
    #         'user': 'root',
    #         'password': 'rjjM1993!',
    #         'host': '127.0.0.1',
    #         'database': 'game_data'
    #     }
    #
    #     # Setup Database connection
    #     mlb_db = mysql.connector.connect(**config)
    #
    #     # Go over the player data and add it to the database
    #     for player_id in data["gameData"]["players"]:
    #         player = data["gameData"]["players"][player_id]
    #         mlb_db_cursor = mlb_db.cursor()
    #
    #         # Check for optional values
    #         draft_year = None
    #         if "draftYear" in player:
    #             draft_year = player["draftYear"]
    #
    #         birth_state = None
    #         if "birthStateProvince" in player:
    #             birth_state = player["birthStateProvince"]
    #
    #         middle_name = None
    #         if "middleName" in player:
    #             middle_name = player["middleName"]
    #
    #         # Generate sql inserts
    #         sql = "insert ignore into game_data.player(id, full_name, first_name, preferred_first_name, middle_name, " \
    #               "last_name, boxscore_name, birth_date, age, birth_city, birth_state, birth_country, height, weight, " \
    #               "is_active, primary_position, is_player, draft_year, bat_hand, throw_hand, strike_zone_top, strike_zone_bottom) values " \
    #               "(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    #         val = (player["id"], player["fullName"], player["firstName"], player["useName"], middle_name,
    #                player["lastName"], player["boxscoreName"], player["birthDate"], player["currentAge"],
    #                player["birthCity"], birth_state, player["birthCountry"], player["height"], player["weight"], player["active"], player["primaryPosition"]["name"],
    #                player["isPlayer"], draft_year, player["batSide"]["description"],
    #                player["pitchHand"]["description"], player["strikeZoneTop"], player["strikeZoneBottom"])
    #
    #         mlb_db_cursor.execute(sql, val)
    #         mlb_db.commit()
    #
    #     mlb_db.close()
    #     print("Done")


if __name__ == '__main__':
    main()


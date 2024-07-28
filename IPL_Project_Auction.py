import random


class Team:
    def __init__(self, name, purse, strategy):
        self.name = name
        self.purse = purse
        self.players = []
        self.strategy = strategy

    def add_player(self, player, price):
        self.players.append(player)
        self.purse -= price

    def make_bid(self, current_price, player_stats, players_needed):
        if self.purse < current_price or players_needed <= 0:
            return 0  # Cannot bid if the purse is less than the current price or no more players needed
        max_bid = self.purse / players_needed  # Ensure they can buy remaining players
        if self.strategy == 'random':
            bid = round(current_price + random.uniform(0.5, min(3.0, max_bid - current_price)), 2)
            return bid if bid <= self.purse else 0
        elif self.strategy == 'conservative':
            bid = round(current_price + 0.5, 2)
            return bid if bid <= self.purse and bid <= max_bid else 0
        elif self.strategy == 'aggressive':
            bid = round(current_price + random.uniform(1.0, min(5.0, max_bid - current_price)), 2)
            return bid if bid <= self.purse else 0
        return 0


class Player:
    def __init__(self, name, base_price, stats):
        self.name = name
        self.base_price = base_price
        self.stats = stats


class Auction:
    def __init__(self, teams, players):
        self.teams = teams
        self.players = players
        self.results = []

    def conduct_auction(self):
        print("Welcome to the IPL auction!")
        for player in self.players:
            self.bid_for_player(player)

    def bid_for_player(self, player):
        current_price = player.base_price
        current_bidder = None
        active_teams = self.teams.copy()
        user_quit = False

        print(f"\nBidding for {player.name} starts at {current_price:.2f} crores.")
        print(f"Stats: {player.stats}")

        user_bid = self.get_valid_bid(
            f"Enter your bid for {player.name} (Base price: {current_price:.2f} crores) or enter 0 to quit: ")
        if user_bid > current_price and user_bid <= next(
                team.purse for team in self.teams if team.name == user_team_name):
            current_price = user_bid
            current_bidder = next(team for team in self.teams if team.name == user_team_name)
            print(f"{current_bidder.name} bids {current_price:.2f} crores for {player.name}")
        else:
            user_bid = 0
            user_quit = True

        while active_teams:
            new_bids = []
            for team in active_teams:
                players_needed = 15 - len(team.players)
                if team.name == user_team_name and user_quit:
                    continue
                elif team.name == user_team_name:
                    if user_bid == 0:
                        active_teams.remove(team)
                else:
                    bid = team.make_bid(current_price, player.stats, players_needed)
                    if bid > current_price:
                        new_bids.append((bid, team))
                        print(f"{team.name} bids {bid:.2f} crores for {player.name}")
                    else:
                        active_teams.remove(team)

            if new_bids:
                current_price, current_bidder = max(new_bids, key=lambda x: x[0])
                if len(new_bids) == 1:
                    active_teams = [new_bids[0][1]]
                if not user_quit:
                    user_bid = self.get_valid_bid(
                        f"Enter your bid for {player.name} (Current highest bid: {current_price:.2f} crores) or enter 0 to quit: ")
                    if user_bid == 0:
                        user_quit = True
                    elif user_bid > current_price and user_bid <= next(
                            team.purse for team in self.teams if team.name == user_team_name):
                        current_price = user_bid
                        current_bidder = next(team for team in self.teams if team.name == user_team_name)
                        print(f"{current_bidder.name} bids {current_price:.2f} crores for {player.name}")
                    else:
                        user_bid = 0
                        user_quit = True
            else:
                break

        if current_bidder:
            current_bidder.add_player(player, current_price)
            self.results.append((player.name, current_bidder.name, current_price))
            print(f"{player.name} sold to {current_bidder.name} for {current_price:.2f} crores.")
        else:
            print(f"{player.name} remains unsold.")
            self.results.append((player.name, "Unsold", 0))

    def get_valid_bid(self, prompt):
        while True:
            try:
                bid = float(input(prompt))
                if bid >= 0:
                    return bid
                else:
                    print("Bid must be a non-negative number. Please try again.")
            except ValueError:
                print("Invalid input. Please enter a valid number.")

    def display_auction_results(self):
        print("\nAuction Results:")
        print(f"{'Player':<20} {'Sold To':<15} {'Price':<10}")
        print("-" * 45)
        for result in self.results:
            player, team, price = result
            print(f"{player:<20} {team:<15} {price:.2f} crores")

    def display_teams_info(self):
        print("\nTeams Info After Auction:")
        for team in self.teams:
            print(
                f"Team: {team.name}, Purse Left: {team.purse:.2f} crores, Players: {[player.name for player in team.players]}")


def get_user_team():
    available_teams = ["RCB", "CSK", "KKR", "MI", "GT"]
    print("Available teams:")
    for team in available_teams:
        print(f"- {team}")
    user_team_name = input("Enter your team name from the above list: ")
    while user_team_name not in available_teams:
        print("Invalid team name. Please choose from the available teams.")
        user_team_name = input("Enter your team name from the above list: ")
    return user_team_name


def initialize_teams(user_team_name):
    strategies = ['random', 'conservative', 'aggressive']
    default_teams = [Team(user_team_name, 30, 'user')]
    available_teams = ["RCB", "CSK", "KKR", "MI", "GT"]
    available_teams.remove(user_team_name)
    for i in range(4):  # Only 4 teams left to initialize
        strategy = random.choice(strategies)
        team = Team(available_teams[i], 30, strategy)
        default_teams.append(team)
    return default_teams


def initialize_players():
    players = [
        Player("Gautam Gambhir", 2.0, {"Runs": 4217, "Average": 31.23, "Strike Rate": 123.88}),
        Player("Sachin Tendulkar", 3.0, {"Runs": 2334, "Average": 33.83, "Strike Rate": 119.82}),
        Player("Rohit Sharma", 4.0, {"Runs": 5230, "Average": 31.31, "Strike Rate": 130.61}),
        Player("Mahendra Singh Dhoni", 5.0, {"Runs": 4632, "Average": 40.25, "Strike Rate": 136.75}),
        Player("Jasprit Bumrah", 6.0, {"Wickets": 109, "Average": 24.54, "Economy Rate": 7.41}),
        Player("Pat Cummins", 7.0, {"Wickets": 38, "Average": 30.13, "Economy Rate": 8.23}),
        Player("Travis Head", 8.0, {"Runs": 205, "Average": 24.41, "Strike Rate": 130.94})
    ]
    return players


# Main function
if __name__ == "__main__":
    user_team_name = get_user_team()
    teams = initialize_teams(user_team_name)
    players = initialize_players()
    auction = Auction(teams, players)
    auction.conduct_auction()
    auction.display_auction_results()
    auction.display_teams_info()



from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand, CommandError
from core.models import Team, Role, UserRole, Coach, Player, Game, UserLoginDetails, TeamStat, PlayerStat
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import get_object_or_404
from faker import Faker


class Command(BaseCommand):
    def team(self, fake):
        for t in range(16):
            try:
                team = Team(name=fake.slug(), abbr=fake.lexify(text='???', letters='ABCDEFGHIJKLMNOPQRSTUVWXYZ'))
            except ObjectDoesNotExist:
                raise CommandError('Team Model Does not exists')
            team.save()
            self.stdout.write(
                self.style.SUCCESS('Successfully inserted Team : "%s" , Abbr : "%s"' % (team.name, team.abbr)))

    def role(self, fake):
        """
            populate role types
        :param fake:
        """
        types = ['C', 'P', 'A']
        for type in range(len(types)):
            try:
                role = Role(type=types[type])
            except ObjectDoesNotExist:
                raise CommandError('Role Model Does not exists')
            role.save()
            self.stdout.write(self.style.SUCCESS('Successfully inserted data for Role "%s"' % role.type))

    def user(self, fake):
        """
            populate users
        :param fake:
        """
        for i in range(177):
            username = fake.user_name()
            password = 'mydemo'
            try:
                user = User.objects.create_user(username=username, email=fake.safe_email(), password=password,
                                                first_name=fake.first_name(), last_name=fake.last_name())
            except ObjectDoesNotExist:
                raise CommandError('User Model Does not exits')
            user.save()
            self.stdout.write(self.style.SUCCESS('User Created : "%s"' % user.username))

    def user_role(self, fake):
        """
            populate user roles as players and coach
        :param fake:
        """
        users = User.objects.filter(is_superuser=False)
        player = get_object_or_404(Role, type='P')
        coach = get_object_or_404(Role, type='C')
        admin = get_object_or_404(Role, type='A')

        # players mapping
        for user in users[:160]:
            try:
                p = UserRole(user_id=user.id, role_id=player.id, is_logged_in=fake.pybool())
            except ObjectDoesNotExist:
                raise CommandError('Issue in adding user role mapping')
            p.save()
            self.stdout.write(self.style.SUCCESS('User Role Mapped : { %s : %s }' % (user.username, player.type)))

        # coach mapping
        for user in users[160:176]:
            try:
                u = UserRole(user_id=user.id, role_id=coach.id, is_logged_in=fake.pybool())
            except coach.DoesNotExists:
                raise CommandError('Issue in adding user role mapping')
            u.save()
            self.stdout.write(self.style.SUCCESS('User Role Mapped : { %s : %s }' % (user.username, coach.type)))

        # super admin
        for user in users[176:]:
            try:
                u = UserRole(user_id=user.id, role_id=admin.id, is_logged_in=fake.pybool())
            except ObjectDoesNotExist:
                raise CommandError('Issue in adding user role mapping')
            u.save()
            self.stdout.write(self.style.SUCCESS('Super Admin Mapped : { %s : %s }' % (user.username, admin.type)))

    def coach(self, fake):
        teams = Team.objects.all()
        coach = Role.objects.filter(type='C').first()
        users = UserRole.objects.filter(role_id=coach.id)

        for i in range(len(teams)):
            try:
                coach = Coach(team_id=teams[i].id, name=fake.slug(), user_id=users[i].user_id)
            except ObjectDoesNotExist:
                raise CommandError('Issue with adding user as Coach')
            coach.save()
            self.stdout.write(self.style.SUCCESS('Coach Created  : %s ' % users[i].user_id))

    def player(self, fake):
        teams = Team.objects.all()
        player = Role.objects.filter(type='P').first()
        users = UserRole.objects.filter(role_id=player.id)

        total = 0
        for team in teams:
            counter = 0
            while counter < 10:
                try:
                    player = Player(team_id=team.id, name=fake.slug(), user_id=users[total].user.id,
                                    height=fake.random_int(min=170, max=255, step=1))
                except ObjectDoesNotExist:
                    raise Warning('Issue with adding user as Player')
                player.save()
                self.stdout.write(self.style.SUCCESS('Player Created  : %s %s' %
                                                     (users[total].user.first_name,
                                                      users[total].user.username)))
                total += 1
                counter += 1

    def qf_game(self, fake):
        teams = Team.objects.all()
        self.create_game(fake, teams, 'QF')

    def sf_game(self, fake):
        teams = Game.objects.filter(round_number='QF')
        self.create_game(fake, teams, 'SF')

    def fi_game(self, fake):
        teams = Game.objects.filter(round_number='SF')
        self.create_game(fake, teams, 'FI')

    def winner(self, fake):
        teams = Game.objects.filter(round_number='FI')
        self.create_game(fake, teams, 'WI')

    def create_game(self, fake, teams, round_number):
        # lets play games
        hosts = teams[1::2]
        guests = teams[0::2]

        # not to self, I can move this and make it a function as well. But it will task for future
        for i in range(len(hosts)):
            host_score = fake.random_int(min=5, max=186, step=1)
            guest_score = fake.random_int(min=5, max=186, step=1)
            winner = hosts[i] if host_score > guest_score else guests[i]

            # lets simplify things so easy to read
            host_id = hosts[i].id if round_number == 'QF' else hosts[i].winner_id
            guest_id = guests[i].id if round_number == 'QF' else guests[i].winner_id
            winner_id = winner.id if round_number == 'QF' else winner.winner_id

            # populate SF teams
            try:
                game = Game(host_id=host_id, guest_id=guest_id, host_score=host_score, guest_score=guest_score,
                            winner_id=winner_id, round_number=round_number,
                            date=fake.date_time_this_decade(before_now=True, after_now=False, tzinfo=None))
            except ObjectDoesNotExist:
                raise CommandError('SF games populated')
            game.save()
            self.stdout.write(self.style.SUCCESS('%s Game %s Vs %s =>  winner : %s '
                                                 % (round_number, host_id, guest_id, winner_id)))

    def user_stat(self, fake):
        users = User.objects.all()

        for user in users:
            for i in range(fake.random_int(min=1, max=10, step=1)):
                stat = UserLoginDetails(user_id=user.id,
                                        login_time=fake.date_time_this_month(before_now=True, after_now=False,
                                                                             tzinfo=None),
                                        logout_time=fake.date_time_this_month(before_now=False, after_now=True,
                                                                              tzinfo=None)
                                        )
                stat.save()
                self.stdout.write(self.style.SUCCESS('Stat saved for  %s ' % user.id))

    def team_stat(self):
        teams = Team.objects.all()

        for team in teams:
            scores = Game.objects.filter(Q(host_id=team.id) | Q(guest_id=team.id))
            for team_score in scores:
                team_id = team_score.host_id if team_score.host_id == team.id else team_score.guest_id
                game_score = team_score.host_score if team_score.host_id == team.id else team_score.guest_score
                # add host stat
                host_stat = TeamStat(score=game_score, game_id=team_score.id, team_id=team_id)
                host_stat.save()
                self.stdout.write(self.style.SUCCESS('Stat saved for Game # %s ' % team_score.id))

    def player_stat(self, fake):
        stats = TeamStat.objects.all()

        for team_stat in stats:
            # this should not be used in production, however this is dummy data to whatever gets jobs done for now
            players = Player.objects.filter(team_id=team_stat.team_id).order_by('?')[:5]
            player_scores = self.generate_random_player_score(5, team_stat.score)

            for i in range(len(players)):
                player_stat = PlayerStat(score=player_scores[i], game_id=team_stat.game_id, player_id=players[i].id)
                player_stat.save()
                self.stdout.write(
                    self.style.SUCCESS('Stat saved for Player # %s : %s ' % (players[i].id, player_scores[i])))

    def generate_random_player_score(self, n, total):
        import random
        dividers = sorted(random.sample(range(1, total), n - 1))
        return [a - b for a, b in zip(dividers + [total], [0] + dividers)]

    def handle(self, *args, **options):
        fake = Faker()

        # lets begin, order is important here

        # initiate team data
        self.team(fake)

        # initiate role data
        self.role(fake)

        # initiate user data
        self.user(fake)
        self.user_role(fake)
        self.user_stat(fake)

        # initiate coach data
        self.coach(fake)

        # initiate player
        self.player(fake)

        # initiate game
        self.qf_game(fake)
        self.sf_game(fake)
        self.fi_game(fake)
        self.winner(fake)

        # init stats data
        self.team_stat()
        self.player_stat(fake)

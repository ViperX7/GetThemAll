from GetThemAll.platforms import ctfd


class pwncollege(ctfd.CTFd):
    def startChall(self, challenge):
        if type(challenge) == int:
            challenge = ctfd.challenge(challenge, self.session, self.url)
        resp = self.session.post(
            self.url + "pwncollege_api/v1/docker",
            json={
                "challenge_id": challenge.export().id,
                "practice": False
            },
            headers={"CSRF-Token": self.get_token()},
        )
        print("\n\n\n")
        print(self.session.cookies)
        print(self.url + 'pwncollege_api/v1/docker')
        print(resp.content)

from GetThemAll.platforms import ctfd


class pwnchall(ctfd.challenge):
    def start(self, id):
        self.session.post(self.url + "/pwncollege_api/v1/docker",
                          json={
                              "challenge_id": self.__id,
                              "practice": False
                          })

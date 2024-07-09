from bs4 import BeautifulSoup
from locust import HttpUser, task,TaskSet, between # type: ignore
from locust import events # type: ignore
import logging

class QuickstartUser(HttpUser):
    wait_time = between(1, 5)

    @task(6)
    def full_post(self):
        proxy_url = "127.0.0.1:8080"
        proxy_dict = {"http": proxy_url, "https": proxy_url}
        with self.client.get('/dashboard', catch_response=True) as dashboard_response:
            if dashboard_response.status_code == 200:
                dashboard_response.success()
            else:
                dashboard_response.failure("[-] dashboard failed")
                return
        with self.client.get('/content/perma?id=102', catch_response=True) as post_response:
            if post_response.status_code == 200:
                post_response.success()
                logging.info("[+]checked the fulled post")
            else:
                post_response.failure("checking post failed")
        
    @task(2)
    def messaging(self):
        proxy_url = "127.0.0.1:8080"
        proxy_dict = {"http": proxy_url, "https": proxy_url}
        with self.client.get('/mail/mail/index', catch_response=True) as mail_response:
            if mail_response.status_code==200:
                mail_response.success()
                logging.info("[+] mail box opened")
                csrf_token = self.extract_csrf_token(mail_response.text,True)
            else:
                mail_response.failure(f"Failed to open mailBox. Status code: {mail_response.status_code}")
                return
            
        with self.client.get('/mail/mail/show?id=2', catch_response=True) as group_response:
            if group_response.status_code==200:
                group_response.success()
                logging.info("[+] chat box opened")
                self.client.headers["X-CSRF-Token"] = csrf_token
                message_data = {
                    "ReplyForm[message]" : "This a message from Locust. from messaging"
                }
            else:
                group_response.failure(f"Failed to open the group. Status code: {group_response.status_code}")
                return
            
        with self.client.post("/mail/mail/reply?id=2",data=message_data, catch_response=True) as message_response:
            if message_response.status_code==200:
                logging.info("[+] messaged something")
                message_response.success()
            else:
                message_response.failure(f"Failed to post comment. Status code: {message_response.status_code}")
        self.client.headers.pop("X-CSRF-Token")  
            
    @task(4)
    def leave_a_comment(self):
        proxy_url = "127.0.0.1:8080"
        proxy_dict = {"http": proxy_url, "https": proxy_url}
        with self.client.get('/dashboard', catch_response=True) as response:
            if response.status_code == 200 and "csrf" in response.text:
                response.success()
                csrf_token = self.extract_csrf_token(response.text, True)
            else:
                response.failure("Couldnt load the dashboard")
                return
        
        with self.client.get("/dashboard/dashboard/stream?StreamQuery%5Bfrom%5D=0&StreamQuery%5Blimit%5D=8",  catch_response=True) as dashboard_update:
            dashboard_update.success()
            object_model = 'humhub\\modules\\polls\\models\\Poll'
            comment_data = {
                "objectModel": object_model,
                "objectId": 19,
                "Comment[message]": "This is an automated comment from Locust. with leaving"
                }
            self.client.headers["X-CSRF-Token"]=csrf_token

        self.client.headers["X-CSRF-Token"]=csrf_token
        with self.client.post("/comment/comment/post",data=comment_data, catch_response=True) as comment_Response:
            if comment_Response.status_code == 200:
                comment_Response.success()
                logging.info("[+] commented something")
            else:
                comment_Response.failure(f"Failed to post comment. Status code: {comment_Response.status_code}")
        self.client.headers.pop("X-CSRF-Token")
        
    @task(1)
    def add_a_movie(self):
        proxy_url = "127.0.0.1:8080"
        proxy_dict = {"http": proxy_url, "https": proxy_url}
        try:
            with self.client.get('/space/browse/search-lazy',  catch_response=True) as space_response:
                if "Movies" in space_response.text:
                    space_response.success()
                    logging.info("Navigated to space directory successfully.")
                else:
                    space_response.failure(f"Failed to navigate to space directory. Status code: {space_response.status_code}")
                    return

            with self.client.get('/s/movies/',  catch_response=True) as movies_response:
                if "/s/movies/about" in movies_response.text:
                    movies_response.success()
                    logging.info("Navigated to movies space successfully.")
                else:
                    movies_response.failure(f"Failed to navigate to specific space. Status code: {movies_response.status_code}")
                    return

            with self.client.get('/s/movies/polls/poll/create-form',  catch_response=True) as form_response:
                if "_csrf" in form_response.text:
                    form_response.success()
                    csrf_token = self.extract_csrf_token(movies_response.text, False)
                    new_movies_data = {
                        "_csrf": csrf_token,
                        "Poll[question]": "Batman Begins 1",
                        "Poll[description]": "![><](https://upload.wikimedia.org/wikipedia/en/a/af/Batman_Begins_Poster.jpg \"Batman Begins\" =260x380)After witnessing his parents' death, Bruce learns the art of fighting to confront injustice. When he returns to Gotham as Batman, he must stop a secret society that intends to destroy the city.",
                        "newAnswers[]": ["Perfect", "Good", "Average", "Not good", "Bad"],
                        "Poll[allow_multiple]": 0,
                        "Poll[is_random]": 0,
                        "Poll[anonymous]": 0,
                        "Poll[show_result_after_close]": 0,
                        "postTopicInput[]": [2, 3, 4],
                        "containerGuid": "3e7693d6-e5c2-4c13-8133-942cd871a9db",
                        "containerClass": "humhub%5Cmodules%5Cspace%5Cmodels%5CSpace",
                        "state": 1
                    }
                else:
                    form_response.failure("form_response failed to find csrf")
                    return

                with self.client.post('/s/movies/polls/poll/create', data=new_movies_data,  catch_response=True) as polls_response:
                    if 'guid' in polls_response.text:
                        logging.info("[+] Added a movie")
                        polls_response.success()
                    else:
                        polls_response.failure(f"Failed to create post. Status code: {polls_response.status_code}")

        except Exception as e:
            logging.exception("An error occurred during the process")
        
    @task(5)
    def Check_movies_space(self):
        proxy_url = "127.0.0.1:8080"
        proxy_dict = {"http": proxy_url, "https": proxy_url}
        with self.client.get('/space/browse/search-lazy', catch_response=True) as jresponse:
            if "Movies" in jresponse.text or "movies" in jresponse.text:
                jresponse.success()
                with self.client.get('/s/movies/', catch_response=True) as space_response:
                    if space_response.status_code == 200:
                        space_response.success()
                        logging.info("[+] movies space checked successful")
                    else:
                        space_response.failure("[-] movies space failed")
            else:
                jresponse.failure(f'[-] space lazy search failed {jresponse.status_code}')

    @task(10)
    def Check_dashboard(self):
        proxy_url = "127.0.0.1:8080"
        proxy_dict = {"http": proxy_url, "https": proxy_url}
        with self.client.get('/dashboard', catch_response=True) as response:
            if response.status_code == 200:
                response.success()
                logging.info("[+] dashboard checked successfully")
            else:
                response.failure("[-] dashboard failed")

    def on_stop(self):
        proxy_url = "127.0.0.1:8080"
        proxy_dict = {"http": proxy_url, "https": proxy_url}
        with self.client.get('/dashboard', catch_response=True) as dresponse:
            if dresponse.status_code == 200:
                csrf_token = self.extract_csrf_token(dresponse.text,True)
                with self.client.post('/user/auth/logout',data={"_csrf":csrf_token}, catch_response=True) as log_response :
                    if "login" in log_response.text:
                        logging.info("[+] Logout successful")
                    else:
                        log_response.failure(f"[-] Logout failed{log_response.status_code}")
            else:
                dresponse.failure(f"failed to load the dashboard{dresponse.status_code}")
                
    def on_start(self):
        proxy_url = "127.0.0.1:8080"
        proxy_dict = {"http": proxy_url, "https": proxy_url}
        #self.client.cookies["XDEBUG_PROFILE"]='1'
        with self.client.get('/user/auth/login', catch_response=True) as Gresponse:
            if Gresponse.status_code == 200:
                csrf_token = self.extract_csrf_token(Gresponse.text,False)
                with self.client.post("/user/auth/login", data={
                                                                "_csrf": csrf_token,
                                                                "Login[username]": "yara.sadeghi.81@gmail.com",
                                                                "Login[password]": "12345",
                                                                "Login[rememberMe]": "1"
                                                                },catch_response=True) as response:
                    if response.status_code==200 and "logout" in response.text:
                        response.success()
                    else:
                        response.failure("[-] Login faild")
            else:
                Gresponse.failure("[-] Couldn't load the login page")

    def extract_csrf_token(self, html_content,isMeta : bool):
        soup = BeautifulSoup(html_content, 'html.parser')
        if isMeta:
            csrf_token = soup.find('meta', {'name': 'csrf-token'})['content']
        else:
            csrf_token = soup.find('input', {'name': '_csrf'})['value']
        return csrf_token









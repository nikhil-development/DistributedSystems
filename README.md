Distributed Systems - Phase 3 Project

Note that we both own M1 and M1 Pro so we required platform: linux/x86_64 in our databases in docker-compose.yml

Enter the main repo:
1. Run command docker-compose down && docker-compose build && docker-compose up
2. database1, database2, database3 gets mounted in this repo (for persistance)
3. For publisher 1, go to http://localhost:5051/publisher_home ; For publisher 2, go to http://localhost:5052/publisher_home ; For publisher 3, go to http://localhost:5053/publisher_home
4. After you go to any one of these publishers, click on Advertise button - it advertises topics that have not been advertised by any publisher yet (you will see the name of the topic) - Do this repeatedly for different topics
5. Once you have advertised a few topics, click on Publish button
6. You can also De-Advertise a topic with the De-Advertise button

7. Next, go to http://localhost:5081/ for subscriber login
8. Login with credentials: Either (username, password) combination of (1,1), (2,2) or (3,3)
9. Once you login, you can click Get All Topics to see the list of available topics - Here, you can choose the topics you (as a subscriber) want to subscribe to
10. You can also click the button at the very bottom to go to a page that shows you the list of the topics you have subscribed to - here, you can check (checkboxes) the topics you would like to unsubscribe to and click the button to execute that
11. With the Get Notified button (here, HTTP Polling), you can stay on the screen - once you publish a new message (with any publisher), and this particular subscriber has subscribed to it, the page automatically shows the new topic message!
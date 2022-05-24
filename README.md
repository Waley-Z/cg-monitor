# Campground Availability Monitor

## About

<!-- With the [Two Course Limit](https://cse.engin.umich.edu/academics/for-current-students/advising/enrollment/) rules for UMich EECS Upper Level courses, if you want to enroll in more than two ULCS courses, you had better pay attention to whether the third one has its waitlist open so that you can get in the list early enough. This script is designed to monitor the open seats of the ULCS courses you want to enroll in. As soon as the available seats become 0 for any lecture or lab session, it will send a notification email. -->

Cloned from [umich-ulcs-monitor](https://github.com/Waley-Z/umich-ulcs-monitor). This program monitors availability of Canyon Campground at Yellowstone National Park.

## Getting Started

- Install `bs4`
    ```bash
    $ pip3 install bs4
    ```

- Configure `SENDER_EMAIL`, `SENDER_PASSWORD`, `RECEPIENT_EMAILS`, and `UPDATE_INTERVAL` in `monitor.py`.

- Run the script

    ```bash
    $ python3 monitor.py
    ```

- To exit, press `Ctrl+C`.

    - If the process failed to exit properly, refer to [this link](https://superuser.com/questions/446808/how-to-manually-stop-a-python-script-that-runs-continuously-on-linux).


## Deployment on Virtual Machine

We can choose to deploy the program on a virtual machine. Popular service providers include [Microsoft Azure Student](https://azure.microsoft.com/en-us/free/students/) and [Amazon AWS Educate](https://aws.amazon.com/education/awseducate/). Given the free credits for students, we can establish a virtual machine for free.

## Using `tmux` to Keep Processes Running

We will use `tmux` to run the program so that it will continue running after the ssh session disconnects. Learn more about other [approaches](https://unix.stackexchange.com/questions/479/keep-processes-running-after-ssh-session-disconnects) and a beginner [guide](https://www.hamvocke.com/blog/a-quick-and-easy-guide-to-tmux/) to `tmux`.

- On your virtual machine, start `tmux` with a new session

  ```bash
  $ ssh azure
  $ tmux
  ```

- Run the program in the session

  ```bash
  $ python3 monitor.py
  ```

- Detach from the session by pressing `C-b d`, which means press `Ctrl+b`, release, and then press `d`. You will get the output

  ```
  [detached (from session 0)]
  ```

- Disconnect ssh as you want

  ```bash
  $ exit
  ```

- After reconnecting to ssh, attach to `tmux` session

  ```bash
  $ ssh azure
  $ tmux attach
  ```

  The program should still be running properly.

## Acknowledgement

- [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/#installing-beautiful-soup)
- [tmux cheatsheet](https://gist.github.com/andreyvit/2921703)

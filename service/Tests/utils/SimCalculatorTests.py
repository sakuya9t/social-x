import unittest


from constant import BATCH_MODE, REALTIME_MODE
from similarity.SimCalculator import SimCalculator
from utils.QueryGenerator import retrieve


class SimCalculatorTests(unittest.TestCase):

    def test_create_calculator(self):
        calculator = SimCalculator()
        self.assertIsNotNone(calculator)

    def test_generate_vector_batch(self):
        account1 = {'platform': 'twitter', 'account': 'tohtohchan'}
        account2 = {'platform': 'instagram', 'account': 'tohtohchan'}
        info1 = retrieve(account1, BATCH_MODE)
        info2 = retrieve(account2, BATCH_MODE)
        info1['platform'] = account1['platform'].lower()
        info2['platform'] = account2['platform'].lower()
        vector = SimCalculator().vectorize(info1, info2, BATCH_MODE)
        print(vector)
        self.assertTrue(len(vector.items()) > 0)

    def test_generate_vector_realtime(self):
        account1 = {'platform': 'twitter', 'account': '1angharad_rees'}
        account2 = {'platform': 'instagram', 'account': 'kaligraphicprint'}
        info1 = retrieve(account1, REALTIME_MODE)
        info2 = retrieve(account2, REALTIME_MODE)
        info1['platform'] = account1['platform'].lower()
        info2['platform'] = account2['platform'].lower()
        vector = SimCalculator().vectorize(info1, info2, REALTIME_MODE)
        print(vector)
        self.assertTrue(len(vector.items()) > 0)

    def test_post_overall_similarity(self):
        posts1 = ['', "THINGS THAT MAKE WRITERS CRY\n- you want to word but the words don't want you\n- it was an amazing movie in your head but a glob on paper\n- something precious was deleted!!!!\n- apparently doing summoning rituals is less effective then, uh, sitting down to just write?? disappointing", 'Morning Coffee Shot - today, yummy Three Beans Coffee in Manly, while I get proofing the print copy of Fire Heart \n \n#writerslife #writingcommunity #ilovesydney', 'Oh! The joy of seeing my comic scripts produced is just the best feeling ever! \n\nSo magical to see frames illustrated exactly as I saw them in my head. \n\nYou illustrators are insanely magical beings  I salut you!! \n#amwriting #ponyhour', 'This is me and my heart tearing in two at the OA news.\n\nGoing to do the movements tonight in hope of travelling to another dimension where @netflix doesn’t mess up and @The_OA continues... \n\n#RenewTheOA', '#writingadvice #writingtips', 'Morning coffee by the lake? Yes please thank you very much! ', 'Read this thread.']
        posts2 = [{'image': 'https://instagram.fcbr1-1.fna.fbcdn.net/vp/16fc2bf10263d266eef9533559ad9383/5E167BB8/t51.2885-15/e35/57299483_130332164728483_4340098046293386214_n.jpg?_nc_ht=instagram.fcbr1-1.fna.fbcdn.net', 'text': 'Wishing a very happy birthday to our teammate Jerome! We hope you have a great day, and a fantastic year ahead!'}, {'image': 'https://instagram.fcbr1-1.fna.fbcdn.net/vp/56f395650c3bb00f9cbf523256cf3b35/5D88AFB1/t51.2885-15/e35/70608634_217062642613493_6161505840013565670_n.jpg?_nc_ht=instagram.fcbr1-1.fna.fbcdn.net', 'text': '“Stroke the Flame'}, {'image': 'https://instagram.fcbr1-1.fna.fbcdn.net/vp/4192a15bc93295b663e4fa80be973901/5DFDFE9A/t51.2885-15/e35/66296876_532514140824095_6927129869739216611_n.jpg?_nc_ht=instagram.fcbr1-1.fna.fbcdn.net', 'text': ''}, {'image': 'https://instagram.fcbr1-1.fna.fbcdn.net/vp/ff4d11117994dc851695193294ca585d/5E30C9D1/t51.2885-15/e35/47582242_296847917703721_332424738263978320_n.jpg?_nc_ht=instagram.fcbr1-1.fna.fbcdn.net', 'text': ''}, {'image': 'https://instagram.fcbr1-1.fna.fbcdn.net/vp/6921ca8b0938e73539c7bf6bd4481d8d/5D882C09/t51.2885-15/e35/67720264_2332986643422865_6016227221794633947_n.jpg?_nc_ht=instagram.fcbr1-1.fna.fbcdn.net', 'text': 'Sound of silence 😂😂😂😂'}]
        sim = SimCalculator().overall_post_sim(posts1, posts2)
        self.assertTrue(0 <= sim <= 1)

    def test_post_max_similarity(self):
        posts1 = ['', "THINGS THAT MAKE WRITERS CRY\n- you want to word but the words don't want you\n- it was an amazing movie in your head but a glob on paper\n- something precious was deleted!!!!\n- apparently doing summoning rituals is less effective then, uh, sitting down to just write?? disappointing", 'Morning Coffee Shot - today, yummy Three Beans Coffee in Manly, while I get proofing the print copy of Fire Heart \n \n#writerslife #writingcommunity #ilovesydney', 'Oh! The joy of seeing my comic scripts produced is just the best feeling ever! \n\nSo magical to see frames illustrated exactly as I saw them in my head. \n\nYou illustrators are insanely magical beings  I salut you!! \n#amwriting #ponyhour', 'This is me and my heart tearing in two at the OA news.\n\nGoing to do the movements tonight in hope of travelling to another dimension where @netflix doesn’t mess up and @The_OA continues... \n\n#RenewTheOA', '#writingadvice #writingtips', 'Morning coffee by the lake? Yes please thank you very much! ', 'Read this thread.']
        posts2 = [{'image': 'https://instagram.fcbr1-1.fna.fbcdn.net/vp/16fc2bf10263d266eef9533559ad9383/5E167BB8/t51.2885-15/e35/57299483_130332164728483_4340098046293386214_n.jpg?_nc_ht=instagram.fcbr1-1.fna.fbcdn.net', 'text': 'Wishing a very happy birthday to our teammate Jerome! We hope you have a great day, and a fantastic year ahead!'}, {'image': 'https://instagram.fcbr1-1.fna.fbcdn.net/vp/56f395650c3bb00f9cbf523256cf3b35/5D88AFB1/t51.2885-15/e35/70608634_217062642613493_6161505840013565670_n.jpg?_nc_ht=instagram.fcbr1-1.fna.fbcdn.net', 'text': '“Stroke the Flame'}, {'image': 'https://instagram.fcbr1-1.fna.fbcdn.net/vp/4192a15bc93295b663e4fa80be973901/5DFDFE9A/t51.2885-15/e35/66296876_532514140824095_6927129869739216611_n.jpg?_nc_ht=instagram.fcbr1-1.fna.fbcdn.net', 'text': ''}, {'image': 'https://instagram.fcbr1-1.fna.fbcdn.net/vp/ff4d11117994dc851695193294ca585d/5E30C9D1/t51.2885-15/e35/47582242_296847917703721_332424738263978320_n.jpg?_nc_ht=instagram.fcbr1-1.fna.fbcdn.net', 'text': ''}, {'image': 'https://instagram.fcbr1-1.fna.fbcdn.net/vp/6921ca8b0938e73539c7bf6bd4481d8d/5D882C09/t51.2885-15/e35/67720264_2332986643422865_6016227221794633947_n.jpg?_nc_ht=instagram.fcbr1-1.fna.fbcdn.net', 'text': 'Sound of silence 😂😂😂😂'}]
        sim = SimCalculator().max_post_sim(posts1, posts2)
        self.assertTrue(0 <= sim <= 1)


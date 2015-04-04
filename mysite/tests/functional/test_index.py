from functional import FunctionalTestCase


class TestIndex(FunctionalTestCase):
    """ Functional test cases for index page
    """

    def test_index_html(self):
        """ A valid html document should be returned when '/' and 'index' is
            accessed. Make sure the html tag and it's children are valid.
        """

        self.browser['ff'].get(self.server_url)

        html_node = self.browser['ff'].find_element_by_tag_name('html')
        self.assertIsNotNone(html_node)

        head_node = html_node.find_element_by_tag_name('head')
        self.assertIsNotNone(head_node)

        body_node = html_node.find_element_by_tag_name('body')
        self.assertIsNotNone(body_node)
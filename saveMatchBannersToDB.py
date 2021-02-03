import compare_banner_links as banner
import database as db


def save_url_banners(url):
    external_links = banner.extract_external_link(url)
    db.insert_to_table('tag_similiar', 'webinfo', f'(url,banners) VALUES("{url}", "{external_links}")')


def match_banners(source_url, destination_url):
    src_select_result = db.select_from_table('tag_similiar', 'webinfo', 'id, banners', f'where url = "{source_url}"')
    src_id = src_select_result[0][0]
    src_links = src_select_result[0][1]
    dest_select_result = db.select_from_table('tag_similiar', 'webinfo', 'id, banners',
                                              f'where url = "{destination_url}"')
    dest_id = dest_select_result[0][0]
    dest_links = dest_select_result[0][1]

    similiar_score = banner.compare_banner_link(src_links, dest_links)
    db.insert_to_table('tag_similiar', 'similiar', f'(src, dest, banner) VALUES({src_id},{dest_id},{similiar_score})')


if __name__ == "__main__":
    match_banners("url1", "url2")

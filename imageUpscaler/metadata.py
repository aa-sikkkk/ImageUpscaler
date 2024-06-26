def preserve_metadata(original_img, processed_img):
    original_metadata = original_img.info
    processed_img.info.update(original_metadata)
    return processed_img

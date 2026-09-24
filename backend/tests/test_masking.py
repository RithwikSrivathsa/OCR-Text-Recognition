from app.core.security import mask_rtsp_url


def test_rtsp_credentials_are_masked():
    masked = mask_rtsp_url("rtsp://user:pass@10.0.0.8:554/stream")
    assert masked == "rtsp://***:***@10.0.0.8:554/stream"

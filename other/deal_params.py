import re

with open("other/params.txt", "r", encoding="utf-8") as f:
    text = f.read()

# 删除连续的Base64字符串（跨多行）
cleaned = re.sub(r"[A-Za-z0-9+/=\n]{350,}", "", text, flags=re.S)
print("cleaned", cleaned)
# with open("other/cleaned.txt", "w", encoding="utf-8") as f:
#     f.write(cleaned)
正页
{
    address = "\U4e2d\U725f\U53bf\U4e09\U5218\U5be8\U6751";
    code = "";
    "curing_quality" = "";
    "engine_no" = 111533;
    "file_number" = "";
    "image_angle" = 0;
    "issue_date" = "2018-03-13";
    kOpenSDKCardResultTypeImage = "<UIImage:0x150860140 anonymous {1376, 932} renderingMode=automatic(original)>";
    kOpenSDKCardResultTypeOriginImage = "<UIImage:0x1508635c0 anonymous {1920, 1080} renderingMode=automatic(original)>";
    "load_quality" = "";
    model = "\U5927\U4f17\U6c7d\U8f66\U724cSVW6474DFD";
    owner = "\U5f20\U7ee2";
    "person_number" = "";
    "plate_no" = "\U8c6bA99RR9";
    "plate_no_second" = "";
    "real_card_type" = "vehicle_license";
    "register_date" = "2018-03-12";
    remarks = "";
    "rotated_image_height" = 932;
    "rotated_image_width" = 1376;
    size = "";
    "test_record" = "";
    "test_valid" = "";
    "total_quality" = "";
    "tow_quality" = "";
    type = "vehicle_license";
    "use_character" = "\U975e\U8425\U8fd0";
    "vehicle_license_seal" = "\U6cb3\U5357\U7701\U90d1\U5dde\U5e02\U516c\U5b89\U5c40\U4ea4\U901a\U8b66\U5bdf\U652f\U961f";
    "vehicle_type" = "\U5c0f\U578b\U666e\U901a\U5ba2\U8f66";
    vin = SSVUDDTT2J2022558;
}
附页
{
    address = "";
    code = 3440020478825;
    "curing_quality" = 8800kg;
    "engine_no" = "";
    "file_number" = 341501707321;
    "image_angle" = 0;
    "issue_date" = "";
    kOpenSDKCardResultTypeImage = "<UIImage:0x150849860 anonymous {1476, 1060} renderingMode=automatic(original)>";
    kOpenSDKCardResultTypeOriginImage = "<UIImage:0x150848aa0 anonymous {1920, 1080} renderingMode=automatic(original)>";
    "load_quality" = "--";
    model = "";
    owner = "";
    "person_number" = "2\U4eba";
    "plate_no" = "";
    "plate_no_second" = "\U4eacN49299";
    "real_card_type" = "vehicle_license";
    "register_date" = "";
    remarks = "\U5f3a\U5236\U62a5\U5e9f\U671f\U6b62:2034-03-12";
    "rotated_image_height" = 1060;
    "rotated_image_width" = 1476;
    size = 6940x2524x3960mm;
    "test_record" = "\U67f4\U6cb9";
    "test_valid" = "2010\U5e7403\U6708";
    "total_quality" = "--";
    "tow_quality" = 40000kg;
    type = "vehicle_license";
    "use_character" = "";
    "vehicle_license_seal" = "";
    "vehicle_type" = "";
    vin = "";
}
import cv2

import utility as utility


class Orb:
    def __init__(self):
        self.orb = cv2.ORB_create(nfeatures=225)
        self.bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    
    def get_features(self, image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        return self.orb.detectAndCompute(gray, None)
    
    def draw_matches(self, img1, kp1, img2, kp2, matches):
        return cv2.drawMatches(img1, kp1, img2, kp2, matches[:50], None, flags=2)
    

def get_matches_from_locations(areas, orb, target_features, target_images, game_image, results):

    game_image = cv2.cvtColor(np.array(game_image), cv2.COLOR_RGB2BGR) 
    game_image = utility.crop_image(game_image, crop_fraction=0.8, preview=False)
    kp2, des2 = orb.get_features(game_image)
    # -=-=-=-=-=-=-=-=- Filter out Impossible Locations -=-=-=-=-=-=-=-=-
    locations = target_features.keys()
    

    location = None
    for loc in locations:
        for ref in target_features[loc].keys():
            try:
                kp1, des1 = target_features[loc][ref]

                # Try with opencv ORB matching
                if des1 is not None and des2 is not None:
                    start = time.time()
                    matches = orb.bf.match(des1, des2)
                    end = time.time()
                    matches = sorted(matches, key=lambda x: x.distance)

                    # print(f"[DEBUG] found {len(matches)} matches for loc {loc}")

                    results[loc]['matches'].append(len(matches))

                    print(f"[DEBUG] {loc} - Matches {len(matches)} - Time: {round(end - start, 3)}")

                    if len(matches) > areas[loc].threshold:
                        print(f"[MATCH] Object matches with {len(matches)} for loc {loc}")
                        print(f"Should Play {areas[loc].tracks}")
                        location = loc
                        # matched_vis = orb.draw_matches(target_images[loc][ref], kp1, game_image, kp2, matches)
                        # cv2.imshow("ORB Match", matched_vis)

            except Exception as e:
                print(f"[ERROR] {e}")
                print(target_images[loc][ref].shape)
                print(game_image.shape)

            if location:
                break
                
                
    return location
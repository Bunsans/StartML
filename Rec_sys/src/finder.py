from heapq import nlargest
import random
import numpy as np
import pandas as pd


def find_neighb(user_target, user_post_like, posts, NUMBER_OF_REC=50):
    NUMBER_OF_NEIGHB = 100
    SMALLEST_NUMBER_OF_INTER = 10

    list_neighb = []
    user_check = set()

    user_target_likes_posts = eval(user_post_like.loc[user_target, "post_like"])
    # can be before
    all_posts = set(posts.unique())
    not_liked_before = all_posts - user_target_likes_posts
    ### should think about posts which user have been viewed, but not liked

    # choice random users for next check
    while len(user_check) < NUMBER_OF_NEIGHB:
        x = random.choice(user_post_like.index)
        if x not in user_check:
            user_check.add(x)

    # There we will know how close user_1 to usr in user_check
    for user_1 in user_check:
        list_neighb.append(
            (
                len(
                    user_target_likes_posts
                    & eval(user_post_like.loc[user_1, "post_like"])
                ),
                user_1,
            )
        )
    # if they intersection is small it is good. Take
    res_nearest = nlargest(SMALLEST_NUMBER_OF_INTER, list_neighb, key=lambda x: x[0])
    res_recom_posts = set()
    count = 0
    for _, neighb in res_nearest:
        # user targ not liked but can be interested
        post = (
            eval(user_post_like.loc[neighb, "post_like"]) - user_target_likes_posts
        ).pop()
        if post not in res_recom_posts and post in not_liked_before:
            res_recom_posts.add(post)
            count += 1
        if count >= NUMBER_OF_REC:
            return res_recom_posts

    # count < NUMBER_OF_REC take not liked posts
    while count < NUMBER_OF_REC:

        post_not_liked = random.choice(posts)
        if post_not_liked not in res_recom_posts and post in not_liked_before:
            res_recom_posts.add(post_not_liked)
            count += 1

    return res_recom_posts


def recomend_finder(
    test_user_id, user_post_like, res_user, res_post_text, time_diff, catboost_model
):
    NUMBER_OF_REC = 50
    posts = res_post_text["post_id"]

    ### making dframe to model

    possible_posts = list(
        find_neighb(test_user_id, user_post_like, posts, NUMBER_OF_REC=50)
    )

    pair_user_posts = np.array([[test_user_id] * NUMBER_OF_REC, possible_posts]).T
    pair_user_posts = pd.DataFrame(pair_user_posts, columns=["user_id", "post_id"])
    data_to_model = pair_user_posts.merge(res_user, on="user_id", how="left").merge(
        res_post_text, on="post_id", how="left"
    )
    time_delta = np.array([time_diff] * NUMBER_OF_REC)
    data_to_model.columns
    data_to_model.insert(len(data_to_model.columns), "time_delta", time_delta)

    ### think about time but later
    # обработать время
    # data_to_model['time_delta']=[80] * NUMBER_OF_REC
    ##################

    data_to_model = data_to_model.drop(["user_id", "post_id"], axis=1)
    predict_model = catboost_model.predict_proba(data_to_model).tolist()
    for i in range(len(predict_model)):
        predict_model[i][0] = possible_posts[i]
    predict_model.sort(reverse=True, key=(lambda x: x[1]))
    result_rec = []
    for preds in predict_model[:5]:
        result_rec.append(preds[0])

    return tuple(result_rec)

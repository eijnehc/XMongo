query_classifier = {
    1: "only_child_axes",
    2: "only_descendant_axes",
    3: "both_child_descendant_axes",
    4: "only_child_axes_with_star",
    5: "only_descendant_axes_with_star",
    6: "only_child_axes_with_single_condition",
    7: "only_child_axes_with_multiple_condition",
    8: "only_child_axes_with_predicates_condition",
}

library_queries = {
    "only_child_axes": {
        1: "/child::library/child::album/child::title",
        2: "/child::library/child::album/child::songs/child::song",
        3: "/child::library/child::album/child::songs/child::song/child::title",
        4: "/library/album/songs/song/title"
    }, 
    "only_descendant_axes": {
        1: "/descendant::title",
        2: "/descendant::song/descendant::title",
        3: "/descendant::songs/descendant::title",
        4: "/descendant::artist",
        5: "/descendant::artists",
        6: "/descendant::songs",
        7: "/descendant::song"
    },
    "both_child_descendant_axes": {
        1: "/child::library/child::album/descendant::song/descendant::title",
        2: "/child::library/child::album/descendant::song/child::title",
        3: "/child::library/descendant::song/child::title",
        4: "/descendant::song/child::title",
    },
    "only_child_axes_with_star": {
        1: "/child::library/child::album/child::*",
        2: "/child::library/child::album/child::songs/child::*",
        3: "/child::library/child::album/child::*/child::song",
        4: "/child::library/child::album/child::*/child::*/child::title",
        5: "/child::library/child::album/child::*/child::*/child::*",
    },
    "only_descendant_axes_with_star": {
        1: "/descendant::*/descendant::title",
        2: "/descendant::*/descendant::song",
        3: "/descendant::*/descendant::name",
        4: "/descendant::*/descendant::*/descendant::name"
    },
    "only_child_axes_with_single_condition": {
        1: "/child::library/child::album[child::title = 'Bua Hati']/child::artists/child::artist",
        2: "/child::library/child::album/child::artists/child::artist[child::country ='Indonesia']",
        3: "/child::library/child::album[child::year = 1997]",
        4: "/child::library/child::album[child::year > 1996]/child::artists/child::artist",
        5: "/child::library/child::album[child::year < 1996]/child::artists/child::artist",
    },
    "only_child_axes_with_multiple_condition": {
        1: "/child::library/child::album[child::title = 'Bua Hati']/child::artists/child::artist[child::country='Indonesia']",
        2: "/child::library/child::album[child::songs/child::song/child::title = 'Miliki Diriku']/child::artists/child::artist[child::country='Indonesia']",
        3: "/library/album[title='Bua Hati']/artists[artist[country='Indonesia']/name='Kris Dayanti']"
    },
    "only_child_axes_with_predicates_condition": { 
        1: "/child::library/child::album[child::year = 1997 or child::year = 1996]/child::artists/child::artist",
        2: "/child::library/child::album[child::year >=  1997 or child::year <= 1996]/child::artists/child::artist",
        3: "/child::library/child::album[child::year = 1997 and child::title = 'No War']/child::artists/child::artist",
        4: "/child::library/child::album[child::title = 'No War' and (child::year = 1997 or child::year = 1996)]/child::artists/child::artist"
    },
}

bookstore_queries = {
    "only_child_axes": {
        1: "/Bookstore/Book/Title",
        2: "/Bookstore/Book/Authors/Author",
        3: "/Bookstore/Book/Authors/Author/First_Name",
    }, 
    "only_descendant_axes": {
        1: "//Title",
        2: "//First_Name"
    },
    "both_child_descendant_axes": {
        1: "/Bookstore/Book/Authors//Author"
    },
    "only_child_axes_with_star": {
        1: "/Bookstore/Book/Author/*",
    },
    "only_descendant_axes_with_star": {
        1: "//*//Title",
        2: "//*//First_Name",
    },
    "only_child_axes_with_single_condition": {
        1: "/Bookstore/Book[@Price < 90]",
        2: "/Bookstore/Book[@Price <= 90]/Title",
        3: "/Bookstore/Book[@Price < 90 and Authors/Author/Last_Name = 'Ullman']/Title",
    }
}
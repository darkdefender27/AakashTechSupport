/**
 * Created by shubham on 11/6/14.
 */

$(function() {

        $('#search').keyup( function(){


                $.ajax({

                        type: "POST",
                        url: "/aakashuser/tags/search/",
                        data: {

                            'search_text':  $('#search').val(),
                            'csrfmiddlewaretoken': $("input[name=csrfmiddlewaretoken]").val
                        },
                        success: searchSuccess,
                        dataType: 'html'

                });

        });
});

function searchSuccess(data, textStatus, jqXHR)
{
    $('search_results').html(data);
}
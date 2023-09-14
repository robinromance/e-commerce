$('.plus-cart').click(function() {
    // Extract the product ID (pid) from the clicked element's attributes
    var id = $(this).attr("pid").toString();

    // Find the element containing the current quantity and store it in 'eml'
    var eml = $(this).parent().children().eq(2);

    // Log the product ID to the console
    console.log("pid =", id);

    // Make an AJAX request to the '/pluscart' URL with the product ID as data
    $.ajax({
        type: 'GET',
        url: '/pluscart',
        data: {
            prod_id: id
        },
        success: function(data) {
            // This function is called when the AJAX request is successful

            // Log the response data to the console
            console.log("data =", data);

            // Update the quantity displayed on the page with the received data
            eml.text(data.quantity);

            // Update the elements with IDs "amount" and "totalamount" with the received data
            $("#amount").text(data.amount);
            $("#totalamount").text(data.totalamount);
        }
    });
});

$('.minus-cart').click(function() {
    // Extract the product ID (pid) from the clicked element's attributes
    var id = $(this).attr("pid").toString();

    // Find the element containing the current quantity and store it in 'eml'
    var eml = $(this).parent().children().eq(2);

    // Log the product ID to the console
    console.log("pid =", id);

    // Make an AJAX request to the '/pluscart' URL with the product ID as data
    $.ajax({
        type: 'GET',
        url: '/minuscart',
        data: {
            prod_id: id
        },
        success: function(data) {
            // This function is called when the AJAX request is successful

            // Log the response data to the console
            console.log("data =", data);

            // Update the quantity displayed on the page with the received data
            eml.text(data.quantity);

            // Update the elements with IDs "amount" and "totalamount" with the received data
            $("#amount").text(data.amount);
            $("#totalamount").text(data.totalamount);
        }
    });
});


$('.remove-cart').click(function(){
    var id=$(this).attr("pid").toString();
    var eml=this
    $.ajax({
        type:'GET',
        url:"/removecart",
        data:{
            prod_id:id
        },
        success:function(data){
            document.getElementById("amount").innerText=data.amount
            document.getElementById("totalamount").innerText=data.totalamount
            eml.parentNode.parentNode.parentNode.parentNode.remove()
        }
    })
})
    


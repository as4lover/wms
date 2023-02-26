$(document).ready(function () {

    $(".increment-btn").click(function (e) { 
        e.preventDefault();
        
        var inc_value = $(this).closest('.product_data').find('.qty-input').val();
        var value = parseInt(inc_value,10);
        value = isNaN(value) ? 0 : value;
        if(value < 40)         
        {
            value++;
            $(this).closest('.product_data').find('.qty-input').val(value)

        }
    }); 

    $(".decrement-btn").click(function (e) { 
        e.preventDefault();
        
        var dec_value = $(this).closest('.product_data').find('.qty-input').val();
        var value = parseInt(dec_value,10);
        value = isNaN(value) ? 0 : value;
        if(value > 1)
        {
            value--;
            $(this).closest('.product_data').find('.qty-input').val(value)

        }
    }); 

    $('.addToCartBtn').click(function (e) { 
        e.preventDefault();
        
        var product_id = $(this).closest('.product_data').find('.prod_id').val();
        var product_qty= $(this).closest('.product_data').find('.qty-input').val();
        var token = $('input[name=csrfmiddlewaretoken]').val();
        $.ajax({
            method: "POST",
            url: "/add-to-cart",
            data: {
                'product_id':product_id,
                'product_qty':product_qty,
                csrfmiddlewaretoken: token
            },
            success: function (response) {
                alertify.success(response.status)
                $('.add_data').load(location.href+' .add_data')
                $('.wishdata').load(location.href+' .wishdata')
            }
        });
    });

    $('.changeQuantity').click(function (e) { 
        e.preventDefault();
        var product_id = $(this).closest('.product_data').find('.prod_id').val();
        var product_qty= $(this).closest('.product_data').find('.qty-input').val();
        var token = $('input[name=csrfmiddlewaretoken]').val();

        $.ajax({
            method: "POST",
            url: "/update-cart",
            data: {
                'product_id': product_id,
                'product_qty': product_qty,
                csrfmiddlewaretoken: token
            },
            success: function (response) {
                // console.log(response)
                alertify.success(response.status)
            }
        });
    });
    
    $(document).on('click','.delete-cart-item', function (e) {
        e.preventDefault();
        var product_id = $(this).closest('.product_data').find('.prod_id').val();
        var token = $('input[name=csrfmiddlewaretoken]').val();

        $.ajax({
            method: "POST",
            url: "delete-cart-item",
            data: {
                'product_id': product_id,
                csrfmiddlewaretoken: token
            },
            success: function (response) {
                alertify.success(response.status)
                $('.cartdata').load(location.href+' .cartdata')
                $('.del_cart').load(location.href+' .del_cart')
                setInterval('location.reload()',1000)
            }
        });
    });
    
    $('.addToWishBtn').click(function (e) { 
        e.preventDefault();
        var product_id = $(this).closest('.product_data').find('.prod_id').val();
        var token = $('input[name=csrfmiddlewaretoken]').val();

        $.ajax({
            method: "POST",
            url: "/add_to_wishlist",
            data: {
                'product_id':product_id,
                csrfmiddlewaretoken: token
            },
            success: function (response) {
                alertify.success(response.status)
                $('.add_wish').load(location.href+' .add_wish')
            },
        });
    });


    $(document).on('click','.delete_wish_item', function (e) {
        e.preventDefault();
        var product_id = $(this).closest('.product_data').find('.prod_id').val();
        var token = $('input[name=csrfmiddlewaretoken]').val();

        $.ajax({
            method: "POST",
            url: "delete_wish_item",
            data: {
                'product_id': product_id,
                csrfmiddlewaretoken: token
            },
            success: function (response) {
                alertify.success(response.status)
                $('.wishdata').load(location.href+' .wishdata')
                $('.del_wish').load(location.href+' .del_wish')
                setInterval('location.reload()',1000)
            }
        });
    });    

    $('.wishToCartBtn').click(function (e) { 
        e.preventDefault();
        var product_id = $(this).closest('.product_data').find('.prod_id').val();
        var token = $('input[name=csrfmiddlewaretoken]').val();

        $.ajax({
            method: "POST",
            url:"/add_wish_to_cart", /*해당 app의 view에서 정의하고 urls에 path에 정의된 url */
            data: {
                'product_id':product_id,
                csrfmiddlewaretoken: token
            },
            success: function (response) {
                alertify.success(response.status)
                $('.add_data').load(location.href+' .add_data')
                },
        });
    });

    $('#myModal').modal({
        backdrop: 'static',
        keyboard: false,
        show: false
      });
      
      $('#myModal').on('shown.bs.modal', function () {
       
          var progress = setInterval(function() {
          var $bar = $('.bar');
      
          if ($bar.width()==500) {
            
              // complete!
              
              // reset progree bar
              clearInterval(progress);
              $('.progress').removeClass('active');
              $bar.width(0);
              
              // update modal 
              $('#myModal .modal-body').html('주문이완료 되었습니다.');
              $('#myModal .hide,#myModal .in').toggleClass('hide in');
              
              // re-enable modal allowing close
              $('#myModal').data('reenable',true);
              $('#myModal').modal('hide');
          } else {
            
              // perform processing logic (ajax) here
              $bar.width($bar.width()+100);
          }
          
        //   $bar.text($bar.width()/5 + "%");
          }, 800);

      });
      
      $('#myModal').on('hidden.bs.modal', function () {
          // reset modal
         if ($('#myModal').data('reenable')) {
             $(this).removeData();
             $('#myModal').modal({
                show: true
             });
         }
      });



});
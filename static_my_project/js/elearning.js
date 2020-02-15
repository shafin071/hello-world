$(document).ready(function(){


	// Contact form AJAX
	var contactForm = $(".contact-form")
	var contactFormMethod = contactForm.attr("method")
	var contactFormEndpoint = contactForm.attr("action")
	
	contactForm.submit(function(event){
		event.preventDefault()
		var contactFormData = contactForm.serialize()
		var thisForm = $(this)
		$.ajax({
			method: contactFormMethod,
			url: contactFormEndpoint,
			data : contactFormData,

			success: function(data){
				$.alert({
						title: "Success!",
						content: data.message,
						theme: "modern",
					})
					contactForm[0].reset()
			},
			error: function(errorData){
				$.alert({
						title: "Oops!",
						content: "Something went wrong!!",
					})
			},

		})
	})


	// Adding and removing courses
	var courseForm = $(".form-course-ajax")
	courseForm.submit(function(event){
		event.preventDefault();

		// assigning $this ensures we are working on the specific form that requested AJAX. So we can use form-course-ajax class in other forms as well and they won't clash
		var thisForm = $(this)

		// Since this AJAX call handles two different snippets, "add to cart" button in course page and the "remove" button cart home. Both buttons lead to update_cart func. I put an if statement, to pick the actionEndpoint based on the page link
		var currentPath = window.location.href

		// indexOf() takes a string and checks the index of it in the http link. If the string is not there, returns -1. So, if cart is in current path, then update cart.
		if(currentPath.indexOf("cart")==-1){
			var actionEndpoint = thisForm.attr("action");
		}
		else{
			// data-endpoint will act as an API service that removes objects from the cart via ajax
			var actionEndpoint = thisForm.attr("data-endpoint");
		}


		var httpMethod = thisForm.attr("method");
		var formData = thisForm.serialize();


		$.ajax({
			url: actionEndpoint,
			method: httpMethod,
			data : formData,

			success: function(data){
				
				var submitSpan = thisForm.find(".submit-span")

				// The html() method sets or returns the content (innerHTML) of the selected elements. innerHTML is a property of submitSpan and it holds the html code of that DOM
				if(data.added){
					submitSpan.html('<button type="submit" class="btn btn-outline-danger btn-lg btn-block">Remove from Cart</button>')
				} else{
					submitSpan.html('<button type="submit" class="btn btn-outline-info btn-lg btn-block">Add to Cart</button><button type="submit" class="btn btn-outline-warning btn-lg btn-block">Buy Now</button>')
				}

				// The text() method sets or returns the text content of the selected elements 
				var navbarCount = $(".navbar-cart-count")
				navbarCount.text(data.cartItemCount)

				if (currentPath.indexOf("cart")!=-1){
					refreshCart()
				}
			},
			error: function(errorData){
				$.alert({
						title: "Oops!",
						content: "Something went wrong",
					})

			},

		})
	})
		
		function refreshCart(){
			var cartTable = $(".cart-table")
			var cartBody = cartTable.find(".cart-body")
			var productRows = cartBody.find(".cart-product")
			var cartTotal = $(".cart-total")
			var currentUrl = window.location.href
			var refreshCartUrl = 'refresh-cart/';

			// getting the refreshed data from the POST data of adding/removing courses from cart
			var refreshCartMethod = "GET";
			var data = {};

			$.ajax({
				url: refreshCartUrl,
				method: refreshCartMethod,
				data: data,

				success: function(data){

					// The remove button needs to be added to cartBody everytime a course is removed
					var hiddenCartItemRemoveForm = $(".cart-item-remove-form")

					if (data.courses.length > 0){
						productRows.html(" ")

						$.each(data.courses, function(index, value){

            			var newCartItemRemove = hiddenCartItemRemoveForm.clone()
            			newCartItemRemove.css("display", "block")
            			newCartItemRemove.find(".cart-course-id").val(value.id)

              			cartBody.append("<tr><td><a class='nav-link' href='" + value.url + "'>" + value.name + "</a></td><td>" + newCartItemRemove.html() + "</td><td>$" +value.price + "</td></tr>")
          			})
						

						cartTotal.text(data.total)
					} else {
						window.location.href = currentUrl
					}
					
				},
				error: function(errorData){
					$.alert({
						title: "Oops!",
						content: "Something went wrong",
					})
			},


			})

		}



        $(".payment-form").hide();
		$('.edit-payment-info').on('click', function(e){
		    $(".payment-form").removeClass('d-none');
		    $(".payment-form").slideDown();
		});
		$('.cancel-payment-form').on('click', function(e){
		    $(".payment-form").slideUp();
		});

        $(".address-form").hide();
		$('.edit-address').on('click', function(e){
		    $(".address-form").slideDown();
		});
		$('.cancel-address-form').on('click', function(e){
		    $(".address-form").slideUp();
		});


        // This is for signup form

        function muteFlag(){
            $('.invalid-feedback').addClass("d-none");
		}

		$('#id_password2').on('input', function(e){
            muteFlag();
		});

		$('#id_username').on('input', function(e){
            muteFlag();
		});

		$('#id_email').on('input', function(e){
            muteFlag();
		});


		// For About this Website Section
		$('.about-this-website').click(function() {
          $('html, body').animate({
            scrollTop: $(".about-this-website-content").offset().top
          }, 500)
        });



})



$(function() {

    $('.cost-items').each(function() {

        var $items = $(this);
        var price = parseFloat($items.attr('data-cost-price')) * 100;
        var cost_const = parseFloat($items.attr('data-cost-const')) * 100;
        var cost_per_item = parseFloat($items.attr('data-cost-per-item')) * 100;

        var decimal_separator = $items.attr('data-decimal-separator');

        var money = function(amount) {
            return amount.toFixed(2).replace(".", decimal_separator);
        }

        var update_costs = function() {
            var items = $items.val();
            if (items < 1)
                items = 1;
            var total_costs = cost_per_item * items + cost_const;
            var final = price * items + total_costs;
            $("#cost-costs").text(money(total_costs / 100) + " zł");
            $("#cost-final").text(money(final / 100) + " zł");
        }

        $items.change(update_costs);
        update_costs();

    });

});

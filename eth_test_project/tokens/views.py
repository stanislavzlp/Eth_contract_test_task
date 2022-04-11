from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Token
from .serializers import TokenSerializer
from .services import generate_new_unique_hash, \
    get_total_supply, send_transaction, StandardPagination


class CreateToken(APIView):
    """
    Takes media_url and owner, send transaction,
    create unique hash and save new token to database
    """

    def post(self, request):
        new_token = TokenSerializer(data=request.data)
        if new_token.is_valid():
            unique_hash = generate_new_unique_hash()
            tx_hash = send_transaction(unique_hash, new_token)

            new_token.save(tx_hash=tx_hash, unique_hash=unique_hash)

            return Response(new_token.data)

        return Response(new_token.errors)


class TokenList(APIView):
    """
    Return list of all Token objects stored in database
    """
    pagination_class = StandardPagination

    def get(self, request):
        tokens = Token.objects.all()
        tokens_serializer = TokenSerializer(tokens, many=True)

        return Response(tokens_serializer.data)


class TokenTotalSupply(APIView):
    """
    Refers to a contract in the blockchain and returns information
    about the current Total Supply - the total number of tokens in the network
    """

    def get(self, request):
        total_supply = get_total_supply()
        result = {
            'total_supply': total_supply
        }
        return Response(result)

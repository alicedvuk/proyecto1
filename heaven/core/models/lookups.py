from django.db.models import Lookup, CharField


class MatchesInsensitive(Lookup):
    lookup_name = 'match'

    def as_sql(self, qn, connection):
        lhs, lhs_params = self.process_lhs(qn, connection)
        rhs, rhs_params = self.process_rhs(qn, connection)

        rhs_params = [''.join(rhs_params).replace('*', '%').replace('?', '_')]
        params = lhs_params + rhs_params

        return '%s ILIKE %s' % (lhs, rhs), params


CharField.register_lookup(MatchesInsensitive)

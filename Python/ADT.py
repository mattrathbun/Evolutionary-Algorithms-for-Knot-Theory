import ADTOp

# Helper function. Takes three numbers: i, m, M. (m meant to be min and M max).
# Returns i if i is between m and M. Otherwise,
#   if i is smaller than m, return m, larger than M, return M


def normalise(i, m, M):
    return (m if i < m else (M if i > M else i))

# In case Matt forgets to use the British spelling.


def normalize(i, m, M):
    return normalise(i, m, M)

# Helper function. Takes a number, positive or negative. If the number
# is even, function returns the index at which that even number shows up
# in a DT-code.  If the number is odd, function returns the index of the
# even number that corresponds to that odd crossing.


def index(num, code):
    if num % 2 == 0:
        return [i for i, j in enumerate(code) if (abs(j) == abs(num))][0]
    elif num % 2 == 1:
        return (abs(num) - 1) / 2
    else:
        raise TypeError("Not in the code.")

# Main class. Encodes a knot diagram by a Dowker-Thistlewaite code,
# augmented by extra data at each crossing as to whether the under-strand
# crosses the over-strand to the left or to the right.  DT-notation is
# generally represented by a list of even numbers, in correspondence with a
# list of ordered odd numbers.  We will encode a DTLink object as two lists:
#
# 1. A list of the even numbers associated with each odd number, c_1,
#    c_2, ... c_{2n-1}; called 'code'.
#    The 'sign' of c_i is positive if the over-strand corresponds to
#    the odd number (2i-1).
#    The 'sign' of c_i is negative if the over-strand corresponds to the
#    even number |c_i|.
# 2. A list of +/-1's, with +1 meaning that the oriented over-strand
#    when rotated counter-clockwise by 90 degrees aligns with the oriented
#    under-strand (regardless of the odd or even labeling), and -1 for
#    vice versa; called 'orientations'
#
#                ^    +1       ^   -1
#                |             |
#             ------>       ---|-->
#                |             |
#
# Additional notes: A number i between 1 and 2n corresponds to both a
# crossing point in the diagram, as well as an oriented edge in the
# diagram going from the point i to the point i+1.


class ADT(object):

    def __init__(self, code, orientations):
        if isinstance(code, list):
            self.code = code
        elif isinstance(code, str):
            self.code = [int(x) for x in code.split()]
        else:
            raise TypeError("Arguments must be either a list or a string.")
        if isinstance(orientations, list):
            self.orientations = orientations
        elif isinstance(orientations, str):
            self.code = [int(x) for x in orientations.split()]
        else:
            raise TypeError("Arguments must be either a list or a string.")
        if len(self.code) != len(self.orientations):
            raise TypeError("Code and Orientations must have the same length.")

    def __eq__(self, other):
        if type(other) == type(self):
            return self.__dict__ == other.__dict__
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def to_list(self):
        return self.code, self.orientations

    # Number of crossings in the diagram is the length of the code.

    def number_crossings(self):
        return len(self.code)

    def copy(self):
        new_dt = []
        new_or = []
        for i in self.code:
            new_dt.append(i)
        for i in self.orientations:
            new_or.append(i)
        return ADT(new_dt, new_or)

    def to_string(self):
        codeString = ", ".join(str(x) for x in self.code)
        orientationsString = ", ".join(str(x) for x in self.orientations)
        return codeString, orientationsString

    # Helper method. Given an integer arc (odd or +/-even), returns a
    # number between 1 and 2*n, with the appropriate modular identification.

    def wrap(self, arc):
        n = self.number_crossings()
        if arc % (2 * n) == 0:
            return 2 * n
        else:
            return arc % (2 * n)

    # Helper method. Given an integer arc, represented by a number at one
    # of the crossings in the diagram (even or odd), returns a 4-element
    # list of the odd number at the crossing; the absolute value of the
    # even number at that crossing; and a +1 or -1 depending on whether
    # the even number is positive or negative (corresponding to whether
    # the even number belongs to under-strand or the over-strand of the
    # diagram, respectively; and a +1 or -1 depending on the orientation
    # of the crossing.

    def quad(self, arc):
        code = self.code
        orient = self.orientations
        n = self.number_crossings()
        arc = normalise(abs(arc), 1, 2 * n)
        if (arc % 2 == 1):
            idx = (arc - 1) / 2
            even = abs(code[idx])
            sign = cmp(code[idx], 0)
            return [arc, even, sign, orient[idx]]
        else:
            even = abs(arc)
            # [0] added so that idx is an integer and not a list.
            # (Else code[idx] does not work.)
#            print "Arc: ", arc
#            print "Code: ", code
#            print "Orientations: ", orient
            idx = [i for i, j in enumerate(code) if abs(j) == even][0]
            odd = 2 * idx + 1
            sign = cmp(code[idx], 0)
            return [odd, even, sign, orient[idx]]

    # Helper method that takes a point at a crossing (odd or +/- even)
    # and returns the other point at that crossing (+even or odd).

    def jump(self, point):
        n = self.number_crossings()
        odd, even, sign, orient = self.quad(point)
        if point % 2 == 1:
            return even
        elif point % 2 == 0:
            return odd

    def isSimple(self):
        n = self.number_crossings()
        if n <= 1:
            return True
        elif n > 1:
            return False
        else:
            raise TypeError(
                "Perhaps this is not a diagram. Something is wrong.")

    # Helper method that takes in an 'arc' and a 'side' ("L" or "R"),
    # and returns a list of all other arcs which are adjacent to the region
    # on the side of the arc indicated by the arguments.
    # These returned arcs are represented as two-element lists, from
    # vertex to vertex (with positive labels).

    # Big Note: regions does not return the correct list when applied to a diagram with only a single crossing.
    # 		In particular, regardless of the side selected, the list will be only a single item long,
    #		indicating only the edge determined by the parameter arc.
    # 		This allows regions to be used correctly with R1 Up/Down moves [CHECK THIS], as well as R3 moves [CHECK THIS],
        #		and R2Down moves, but NOT with R2Up moves.

    def regions(self, arc, side):
        side = str(side).lower()
        if side in ["l", "left", "0", "L"]:
            side = 0
        elif side in ["r", "right", "1", "R"]:
            side = 1
        else:
            raise TypeError("Side should be 'L' or 'R'.")
        forward = 0
        once = 0
        output = []
        n = self.number_crossings()
        if n == 0:
            return output
        elif n == 1:
            return [[1, 2]]
        arc = normalise(arc, 1, 2 * n)
        tail = arc
        head = self.wrap(arc + 1)
#        if n == 1:
#        	output = [[tail, head], [head, tail]] ###############################
#        else:
        while True:
            tail = self.jump(head)
            odd, even, sign, orient = self.quad(tail)
            if ((side + forward) % 2 == 0) and (tail % 2 == 1):
                head = self.wrap(tail - sign * orient)
            elif ((side + forward) % 2 == 0) and (tail % 2 == 0):
                head = self.wrap(tail + sign * orient)
            elif ((side + forward) % 2 == 1) and (tail % 2 == 1):
                head = self.wrap(tail + sign * orient)
            elif ((side + forward) % 2 == 1) and (tail % 2 == 0):
                head = self.wrap(tail - sign * orient)
            output.append([tail, head])
            if (tail == arc and head == self.wrap(arc + 1)):
                break
            if ((tail - head) % (2 * n) == 1):
                forward = 1
            else:
                forward = 0
        return output

    # Method which shifts the labeling of a diagram by one (with the same orientation) to return
    # a new ADT object with a different code representing the diagram.

    def shiftLabel(self):
        new_code = []
        new_orients = []
        temp = []
        for i in self.code:
            odd, even, sign, orient = self.quad(i)
            temp.append(
                [self.wrap(even - 1), self.wrap(odd - 1), -sign, orient])
        temp.sort()
        for i in temp:
            new_code.append(i[2] * i[1])
            new_orients.append(i[3])
        return ADT(new_code, new_orients)

    # Method which tests whether two codes correspond to the same diagram by testing all
    # the label-shifts of K.

    def sameDiagram(self, K):
        #    	print "    Calling sameDiagram."
        n = self.number_crossings()
        m = K.number_crossings()
        if n != m:
            #    		print "        Different number of crossings!"
            return False
        elif n == 0:
            return True
        else:
            around = K.copy()
            for i in range(2 * n + 1):
                if around == self:
                    #    				print "    An exact match."
                    return True
#    				print "THIS LINE SHOULD NEVER BE PRINTED."
                else:
                    #    				print "    Not an exact match."
                    #    				print "    ", self.to_string(), " is not equal to ", around.to_string()
                    #    				print "    Let's try shifting labels."
                    around = around.shiftLabel()
            return False

    # Methods that perform a Reidemeister 1 Move, introducing a single
    # twist at the location arc.  arc is an integer corresponding to a
    # label at one of the crossings of the diagram.  The twist should
    # be introduced in the arc that immediately PROcedes the label arc
    # (the arc which connects the point arc to the point arc+1).
    # Method mutates the ADT object, and returns True if the move
    # is successfully performed (which it always should since an R1Up
    # move has no obstruction).

    def R1Up(self, arc, side, sign):
        if side == "L":
            side = 1
        elif side == "R":
            side = -1
        else:
            raise TypeError("Side should be 'L' or 'R'.")
        n = self.number_crossings()
        arc = normalise(arc, 1, 2 * n)
        new_dt = []
        new_or = list(self.orientations)
        for i in self.code:
            if abs(i) > arc:
                new_dt.append(i + 2 * cmp(i, 0))
            else:
                new_dt.append(i)
        if arc % 2 == 1:
            new_dt.insert((arc + 1) / 2, side * sign * (arc + 1))
            new_or.insert((arc + 1) / 2, sign)
        else:
            new_dt.insert(arc / 2, -side * sign * (arc + 2))
            new_or.insert(arc / 2, sign)
        self.code = new_dt
        self.orientations = new_or
        return True

    # Methods that perform a Reidemeister 1 Move, eliminating a single
    # twist at the location arc.  Method mutates the ADT object,
    # returns True if move is successfully performed (the move will be
    # unsuccessful if the diagram does not contain a positive twist at
    # the location arc, i.e. if a (positive) even number in the code
    # corresponds to an adjacent (odd) number.)

    def R1Down(self, arc):
        if len(self.regions(arc, "L")) == 1:
            side = 1
        elif len(self.regions(arc, "R")) == 1:
            side = -1
        else:
            return False
        n = self.number_crossings()
        arc = normalise(arc, 1, 2 * n)
        if arc == 2*n:
        	K = self.shiftLabel()
        	self.code = K.code
        	self.orientations = K.orientations
        	arc = self.wrap(arc - 1)
        new_dt = []
        temp_dt = list(self.code)
        new_or = list(self.orientations)
        if arc % 2 == 1:
            temp_dt.pop(((arc - 1) / 2) % n)
            for i in temp_dt:
                if abs(i) > arc + 1:
                    new_dt.append(i - 2 * cmp(i, 0))
                else:
                    new_dt.append(i)
            self.code = new_dt
            self.orientations.pop(((arc - 1) / 2) % n)
            return True
        elif arc % 2 == 0:
            temp_dt.pop((arc / 2) % n)
#            print "temp_dt is: ", temp_dt
            for i in temp_dt:
                if abs(i) > arc:
                    new_dt.append(i - 2 * cmp(i, 0))
                else:
                    new_dt.append(i)
#            print "new_dt has become: ", new_dt
            self.code = new_dt
            self.orientations.pop((arc / 2) % n)
            return True

    # Methods that perform a Reidemeister 2 Move, introducing two
    # additional crossings.
    #   arc -- is an integer corresponding to a label at one of the
    #     crossings of the diagram, indicating the edge from arc to arc+1
    #     (or rather, wrap(arc+1)).
    #   side -- is a choice of 'l' or 'r' to determine to which side of
    #     arc in the diagram arc will be perturbed to introduce the
    #     additional crossings with another strand.
    #   target -- is a two-element list [tail, head].
    #     [tail, head] -- is the other strand that arc will cross over
    #     or under.
    #
    # Method mutates the ADT object, and returns True if the move
    # is successfully performed.

    # Note: The parity of arc will be the same as the parity of tail,
    # if [tail, head] represents an edge adjacent to a region determined
    # by arc.

    # Note: Specifying the whether the new crossings should go over or
    # under is unnecessary as pushing (arc, arc+1) under (tail, head)
    # is equivalent to pushing (tail, head) over (arc, arc+1). We have arbitrarily chosen
    # to push (arc, arc+1) OVER (tail, head).

    # Big Note: The regions method does not return the correct output on diagrams with
    # a single crossing. As this only effects the outcome of the R2Up method, it appears
    # to be easier to modify the behavior of R2Up in this special case instead of the
    # regions method itself.

    def R2Up(self, arc, side, target):
    	count = 0
        n = self.number_crossings()
        # This is where the R2Up move is precluded from being applied to a
        # single-crossing diagram.
        if n <= 1:
            return False
        arc = normalise(arc, 1, 2 * n)
        new_arc = arc
        candidates = list(self.regions(arc, side))
        candidates.remove([arc, self.wrap(arc + 1)])
        if not(target in candidates):
            return False
        new_dt = []
        new_or = list(self.orientations)
        tail, head = target
        if side in ['L', 'l', 'left', '0', 'Left']:
            side = 1
        elif side in ['R', 'r', 'right', '1', 'Right']:
            side = -1
        else:
            raise TypeError("Side should be 'L' or 'R'.")
        K = self.copy()
        while new_arc != 2*n:
        	count += 1
        	print "Shifting label...{} times so far.".format(count)
        	K = K.shiftLabel()
        	new_arc = K.wrap(new_arc - 1)
        	tail = K.wrap(tail - 1)
        	head = K.wrap(head - 1)
        print "Tail and Head are ", tail, head
        if tail == K.wrap(head + 1):
        	new_code = [i+(2*cmp(i, 0)) if abs(i) > head else i for i in K.code]
        	new_orientations = [i for i in K.orientations]
        	new_code.append(K.wrap(head + 1))
        	new_orientations.append(-side)
        	new_code.insert((head + 1)/2, -(2*n + 4))
        	new_orientations.insert((head + 1)/2, side)
        if head == self.wrap(tail + 1):
        	new_code = [i+(2*cmp(i, 0)) if abs(i) > tail else i for i in K.code]
        	print "K orientations: ", K.orientations
        	new_orientations = [i for i in K.orientations]
        	print "new_code, new_orientations: ", new_code, new_orientations
        	new_code.append(K.wrap(tail + 2))
        	new_orientations.append(side)
        	print "new_code, new_orientations: ", new_code, new_orientations
        	new_code.insert(tail/2, -(2*n + 4))
        	new_orientations.insert(tail/2, -side)
        	print "new_code, new_orientations: ", new_code, new_orientations
        self.code = new_code
        self.orientations = new_orientations
        	

#     def R2Up(self, arc, side, target):
#         n = self.number_crossings()
#         # This is where the R2Up move is precluded from being applied to a
#         # single-crossing diagram.
#         if n <= 1:
#             return False
#         arc = normalise(arc, 1, 2 * n)
#         candidates = list(self.regions(arc, side))
#         candidates.remove([arc, self.wrap(arc + 1)])
#         if not(target in candidates):
#             return False
#         new_dt = []
#         new_or = list(self.orientations)
#         tail, head = target
#         if side in ['L', 'l', 'left', '0', 'Left']:
#             side = 1
#         elif side in ['R', 'r', 'right', '1', 'Right']:
#             side = -1
#         else:
#             raise TypeError("Side should be 'L' or 'R'.")
#         if arc % 2 == 0:
#             if arc < tail:
#                 if head == self.wrap(tail + 1):
#                     print "Case 1"
#                     for i in self.code:
#                         if (abs(i) > arc) and (abs(i) > tail):
#                             new_dt.append(i + 4 * cmp(i, 0))
#                         elif (abs(i) > arc):
#                             new_dt.append(i + 2 * cmp(i, 0))
#                         else:  # abs(i) <= arc
#                             new_dt.append(i)
#                     new_dt.insert(arc / 2, tail + 4)
#                     new_or.insert(arc / 2, side)
#                     new_dt.insert(tail / 2 + 1, -(arc + 2))
#                     new_or.insert(tail / 2 + 1, -side)
#                 else:  # tail == self.wrap(head + 1)
#                     print "Case 2"
#                     for i in self.code:
#                         if (abs(i) > arc) and (abs(i) >= tail):
#                             new_dt.append(i + 4 * cmp(i, 0))
#                         elif (abs(i) > arc):
#                             new_dt.append(i + 2 * cmp(i, 0))
#                         else:  # abs(i) <= arc
#                             new_dt.append(i)
#                     new_dt.insert(arc / 2, tail + 2)
#                     new_or.insert(arc / 2, -side)
#                     new_dt.insert(tail / 2 + 1, -(arc + 2))
#                     new_or.insert(tail / 2 + 1, side)
#             else:  # tail < arc
#                 if head == self.wrap(tail + 1):
#                     print "Case 3"
#                     for i in self.code:
#                         if (abs(i) > arc):
#                             new_dt.append(i + 4 * cmp(i, 0))
#                         elif (abs(i) > tail):  # but <= arc
#                             new_dt.append(i + 2 * cmp(i, 0))
#                         else:  # abs(i) <= tail
#                             new_dt.append(i)
#                     new_dt.insert(tail / 2, -(arc + 4))
#                     new_or.insert(tail / 2, -side)
#                     new_dt.insert(arc / 2 + 1, tail + 2)
#                     new_or.insert(arc / 2 + 1, side)
#                 else:  # head < tail
#                     print "Case 4"
#                     for i in self.code:
#                         if (abs(i) > arc):
#                             new_dt.append(i + 4 * cmp(i, 0))
#                         elif (abs(i) >= tail):  # but <= arc
#                             new_dt.append(i + 2 * cmp(i, 0))
#                         else:  # abs(i) < tail
#                             new_dt.append(i)
#                     new_dt.insert(tail / 2, -(arc + 4))
#                     new_or.insert(tail / 2, side)
#                     new_dt.insert(arc / 2 + 1, tail)
#                     new_or.insert(arc / 2 + 1, -side)
#         else:  # arc % 2 == 1
#             if arc < tail:
#                 if head == self.wrap(tail + 1):
#                     print "Case 5"
#                     for i in self.code:
#                         if abs(i) > tail:
#                             new_dt.append(i + 4 * cmp(i, 0))
#                         elif abs(i) > arc:  # but <= tail
#                             new_dt.append(i + 2 * cmp(i, 0))
#                         else:  # abs(i) <= arc
#                             new_dt.append(i)
#                     new_dt.insert((arc + 1) / 2, head + 2)
#                     new_or.insert((arc + 1) / 2, -side)
#                     new_dt.insert(head / 2 + 1, -(arc + 1))
#                     new_or.insert(head / 2 + 1, side)
#                 else:  # tail == self.wrap(head + 1)
#                     print "Case 6"
#                     for i in self.code:
#                         if abs(i) >= tail:
#                             new_dt.append(i + 4 * cmp(i, 0))
#                         elif abs(i) > arc:  # but < tail
#                             new_dt.append(i + 2 * cmp(i, 0))
#                         else:  # abs(i) <= arc
#                             new_dt.append(i)
#                     new_dt.insert((arc + 1) / 2, head + 4)
#                     new_or.insert((arc + 1) / 2, side)
#                     new_dt.insert(head / 2 + 1, -(arc + 1))
#                     new_or.insert(head / 2 + 1, -side)
#             else:  # tail < arc
#                 if head == self.wrap(tail + 1):
#                     print "Case 7"
#                     for i in self.code:
#                         if abs(i) > arc:
#                             new_dt.append(i + 4 * cmp(i, 0))
#                         elif abs(i) > tail:  # but <= arc
#                             new_dt.append(i + 2 * cmp(i, 0))
#                         else:  # abs(i) <= tail
#                             new_dt.append(i)
#                     new_dt.insert(head / 2, -(arc + 3))
#                     new_or.insert(head / 2, side)
#                     new_dt.insert((arc + 1) / 2 + 1, tail + 1)
#                     new_or.insert((arc + 1) / 2 + 1, -side)
#                 else:  # tail == self.wrap(head + 1)
#                     print "Case 8"
#                     for i in self.code:
#                         if abs(i) > arc:
#                             new_dt.append(i + 4 * cmp(i, 0))
#                         elif abs(i) >= tail:  # but <= arc
#                             new_dt.append(i + 2 * cmp(i, 0))
#                         else:  # abs(i) < tail
#                             new_dt.append(i)
#                     new_dt.insert(head / 2, -(arc + 3))
#                     new_or.insert(head / 2, -side)
#                     new_dt.insert((arc + 1) / 2 + 1, tail + 1)
#                     new_or.insert((arc + 1) / 2 + 1, side)
#         self.code = new_dt
#         self.orientations = new_or
#         return True

    # Methods that perform a Reidemeister 2 Move, eliminating two crossings.
    # A pre-condition for this move is the existence of a bigon in which
    # crossings have opposite 'orientations'.
    #   arc -- is an integer corresponding to a label at one of the
    #     crossings of the diagram, indicating the edge from arc to arc+1
    #     (or rather, wrap(arc+1)).
    #
    # Note: This is enough information to determine the location of an
    # R2Down move, because the pre-condition for such a move is the
    # existence of a certain type of bigon, and such a bigon means that
    # there is no choice of secondary arc, and the edge can only be
    # adjacent to at most one bigon.
    #
    # Method mutates the ADT object, and returns True if the move
    # is successfully performed.
    #
    # Note also, the parity of arc will be the same as the parity of tail,
    # if [tail, head] represents an edge adjacent to a region determined
    # by arc.
    #
    # Please also note that R2DownPlus (and probably R2UpPlus) do not
    # take negative arc arguments.
    # Does not play nice with normalise.

    def R2Down(self, arc):
        n = self.number_crossings()
        arc = normalise(arc, 1, 2 * n)
        candidates_left = list(self.regions(arc, 'L'))
        candidates_right = list(self.regions(arc, 'R'))
        if len(candidates_left) == 2:
            candidates = candidates_left
        elif len(candidates_right) == 2:
            candidates = candidates_right
        else:
            return False
        candidates.remove([arc, self.wrap(arc + 1)])
        i1 = index(arc, self.code)
        i2 = index(self.wrap(arc + 1), self.code)
        I = max(i1, i2)
        i = min(i1, i2)
        o1 = self.orientations[i1]
        o2 = self.orientations[i2]
        if o1 != -o2:
            return False
        elif n == 2:
            self.code = []
            self.orientations = []
            return True
        new_code = []
        tail, head = candidates[0]
        if abs(abs(arc) - abs(self.wrap(arc + 1))) == 1 and abs(abs(tail) - abs(head)) == 1:
            m = min(abs(tail), abs(head), abs(arc))
            M = max(abs(tail), abs(head), abs(arc))
            del self.code[I]
            del self.orientations[I]
            del self.code[i]
            del self.orientations[i]
            for j in self.code:
                if abs(j) < m:
                    new_code.append(j)
                elif m < abs(j) and abs(j) < M:
                    new_code.append(j - 2 * cmp(j, 0))
                else:
                    new_code.append(j - 4 * cmp(j, 0))
        else:
            l = [abs(arc), abs(self.wrap(arc + 1)), abs(tail), abs(head)]
            l.sort()
            m = l[1]
            M = l[2]
            del self.code[I]
            del self.orientations[I]
            del self.code[i]
            del self.orientations[i]
            for j in self.code:
                if abs(j) < M:
                    new_code.append(j)
                else:
                    new_code.append(j - 2 * cmp(j, 0))
            new_code.insert(0, new_code.pop())
            self.orientations.insert(0, self.orientations.pop())
        self.code = new_code
        return True

    # helper

    def isOdd(self, arc):
        return arc % 2 == 1

    # helper

    def isOverstrand(self, arc):
        if self.isOdd(arc) and self.quad(arc)[2] == -1:
            return False
        if self.isOdd(arc) and self.quad(arc)[2] == 1:
            return True
        if not self.isOdd(arc) and self.quad(arc)[2] == -1:
            return True
        if not self.isOdd(arc) and self.quad(arc)[2] == 1:
            return False

    # helper: returns the crossing to the right of the current arc
    def right(self, arc):
        if self.isOverstrand(arc) and self.quad(arc)[3] == -1:
            return self.wrap(self.jump(arc) + 1)
        if self.isOverstrand(arc) and self.quad(arc)[3] == +1:
            return self.wrap(self.jump(arc) - 1)
        if not self.isOverstrand(arc) and self.quad(arc)[3] == -1:
            return self.wrap(self.jump(arc) - 1)
        if not self.isOverstrand(arc) and self.quad(arc)[3] == +1:
            return self.wrap(self.jump(arc) + 1)

    # helper: returns the crossing to the left of the current arc

    def left(self, arc):
        if self.isOverstrand(arc) and self.quad(arc)[3] == -1:
            return self.wrap(self.jump(arc) - 1)
        if self.isOverstrand(arc) and self.quad(arc)[3] == +1:
            return self.wrap(self.jump(arc) + 1)
        if not self.isOverstrand(arc) and self.quad(arc)[3] == -1:
            return self.wrap(self.jump(arc) + 1)
        if not self.isOverstrand(arc) and self.quad(arc)[3] == +1:
            return self.wrap(self.jump(arc) - 1)

    # Helper. Determines whether the arc going to the right of
    # the specified arc is "pointing outwards" (away from the arc)
    # or "inwards"

    def rightOutwards(self, arc):
        if self.isOverstrand(arc) and self.quad(arc)[3] == -1:
            return True
        if self.isOverstrand(arc) and self.quad(arc)[3] == +1:
            return False
        if not self.isOverstrand(arc) and self.quad(arc)[3] == -1:
            return False
        if not self.isOverstrand(arc) and self.quad(arc)[3] == +1:
            return True

    # Helper. Determines whether the arc going to the right of the
    # specified arc is "pointing outwards" (away from the arc) or
    # "inwards"

    def leftOutwards(self, arc):
        if self.isOverstrand(arc) and self.quad(arc)[3] == +1:
            return True
        if self.isOverstrand(arc) and self.quad(arc)[3] == -1:
            return False
        if not self.isOverstrand(arc) and self.quad(arc)[3] == +1:
            return False
        if not self.isOverstrand(arc) and self.quad(arc)[3] == -1:
            return True

    # The R3 move
    def R3(self, arc, side):
        n = self.number_crossings()
        arc = normalise(arc, 1, 2 * n)
        arcNext = self.wrap(arc + 1)

        if self.right(arc) != self.jump(self.right(arcNext)):
            # print "cannot do R3 from that position: not a triangle"
            return False

        if self.quad(arc)[2] == self.quad(arcNext)[2]:
            # not both over or undercrossings
            # print "Not both overcrossings or undercrossings"
            return False
        doubleOverstrand = self.isOverstrand(arc)
        #print "DO: ", doubleOverstrand
        #print "RR: ", self.right(arc), self.right(arcNext)

        rewrite = {}
        if side in ['R', 'r', 'right', '1', 'Right']:
            # rewrite the crossing
            # the crossing is _always_ changed in sign
            if self.rightOutwards(arc):
                rewrite.update(
                    {self.right(arc): -self.wrap(self.right(arc) - 1)})
            else:
                rewrite.update(
                    {self.right(arc): -self.wrap(self.right(arc) + 1)})
            if self.rightOutwards(arcNext):
                rewrite.update(
                    {self.right(arcNext): -self.wrap(self.right(arcNext) - 1)})
            else:
                rewrite.update(
                    {self.right(arcNext): -self.wrap(self.right(arcNext) + 1)})
            # rewrite the strand part 1
            if self.rightOutwards(arcNext):
                rewrite.update(
                    {self.jump(arc): self.wrap(self.jump(arcNext) + 1)})
            else:
                rewrite.update(
                    {self.jump(arc): self.wrap(self.jump(arcNext) - 1)})
            # rewrite the strand part 2
            if self.rightOutwards(arc):
                rewrite.update(
                    {self.jump(arcNext): self.wrap(self.jump(arc) + 1)})
            else:
                rewrite.update(
                    {self.jump(arcNext): self.wrap(self.jump(arc) - 1)})
            theCrossing = abs(self.right(arc))
            if not self.isOdd(theCrossing):
                theCrossing = abs(self.jump(self.right(arc)))

        if (side in ['L', 'l', 'left', '0', 'Left']):
            # rewrite the crossing
            # the crossing is _always_ changed in sign
            if self.leftOutwards(arc):
                rewrite.update(
                    {self.left(arc): -self.wrap(self.left(arc) + 1)})
            else:
                rewrite.update(
                    {self.left(arc): -self.wrap(self.left(arc) - 1)})
            if self.leftOutwards(arcNext):
                rewrite.update(
                    {self.left(arcNext): -self.wrap(self.left(arcNext) + 1)})
            else:
                rewrite.update(
                    {self.left(arcNext): -self.wrap(self.left(arcNext) - 1)})
            # rewrite the strand part 1
            if self.leftOutwards(arcNext):
                rewrite.update(
                    {self.jump(arc): self.wrap(self.jump(arcNext) - 1)})
            else:
                rewrite.update(
                    {self.jump(arc): self.wrap(self.jump(arcNext) + 1)})
            # rewrite the strand part 2
            if self.leftOutwards(arc):
                rewrite.update(
                    {self.jump(arcNext): self.wrap(self.jump(arc) - 1)})
            else:
                rewrite.update(
                    {self.jump(arcNext): self.wrap(self.jump(arc) + 1)})
            theCrossing = abs(self.left(arc))
            if not self.isOdd(theCrossing):
                theCrossing = abs(self.jump(self.left(arc)))

#        print "\nfinal rewrite: ", rewrite, "\n"

        # it helps that rewrite[even] = odd and vice versa
        newCode = [0] * self.number_crossings()
        pairs = []
        for i in range(1, 2 * self.number_crossings(), 2):
            pairs.append(map(lambda x: (rewrite[x] if x in rewrite else x)
                             if x > 0 else (-rewrite[-x] if -x in rewrite else x), [i, self.code[(i - 1) / 2]]))

        for p in pairs:
            crossingSign = 1
            if p[0] < 0 or p[1] < 0:
                crossingSign = -1
            print "p ",p,"  crossing sign", crossingSign
            if self.isOdd(p[0]):
                newCode[(abs(p[0]) - 1) / 2] = crossingSign * abs(p[1])
            else:
                newCode[(abs(p[1]) - 1) / 2] = crossingSign * abs(p[0])
        self.code = newCode

        theNewCrossing = self.jump(rewrite[theCrossing])

        # orientations
        temp = self.orientations[index(theCrossing, self.code)]
        self.orientations[index(theCrossing, self.code)] = self.orientations[
            index(theNewCrossing, self.code)]
        self.orientations[index(theNewCrossing, self.code)] = temp

        return True

# Generates a list of possible moves that can be performed on a diagram.
    def finePossibleMoves(self):
        possible_moves = []
        n = self.number_crossings()
        if n == 0:
            possible_moves.append(
                ADTOp.ADTOp(1, 'U', {'arc': 1, 'side': 'L', 'sign': 1}))
            possible_moves.append(
                ADTOp.ADTOp(1, 'U', {'arc': 1, 'side': 'L', 'sign': -1}))
            possible_moves.append(
                ADTOp.ADTOp(1, 'U', {'arc': 1, 'side': 'R', 'sign': 1}))
            possible_moves.append(
                ADTOp.ADTOp(1, 'U', {'arc': 1, 'side': 'R', 'sign': -1}))
            return possible_moves
        for i in range(1, 2 * n + 1):
            possible_moves.append(
                ADTOp.ADTOp(1, 'U', {'arc': i, 'side': 'L', 'sign': 1}))
            possible_moves.append(
                ADTOp.ADTOp(1, 'U', {'arc': i, 'side': 'L', 'sign': -1}))
            possible_moves.append(
                ADTOp.ADTOp(1, 'U', {'arc': i, 'side': 'R', 'sign': 1}))
            possible_moves.append(
                ADTOp.ADTOp(1, 'U', {'arc': i, 'side': 'R', 'sign': -1}))
            left_reg = len(self.regions(i, 'L'))
            right_reg = len(self.regions(i, 'R'))
            if left_reg == 1 or right_reg == 1:
                possible_moves.append(ADTOp.ADTOp(1, 'D', {'arc': i}))
            # This precludes listing R2Up moves on a single-crossing or
            # no-crossing diagram.
            if left_reg > 1 and n > 1:
                candidates = list(self.regions(i, 'L'))
                candidates.remove([i, self.wrap(i + 1)])
                for j in candidates:
                    possible_moves.append(
                        ADTOp.ADTOp(2, 'U', {'arc': i, 'side': 'L', 'target': j}))
            # This precludes listing R2Up moves on a single-crossing or
            # no-crossing diagram.
            if right_reg > 1 and n > 1:
                candidates = list(self.regions(i, 'R'))
                candidates.remove([i, self.wrap(i + 1)])
                for j in candidates:
                    possible_moves.append(
                        ADTOp.ADTOp(2, 'U', {'arc': i, 'side': 'R', 'target': j}))
            if (left_reg == 2 or right_reg == 2) and n > 1:
                i1 = index(i, self.code)
                i2 = index(self.wrap(i + 1), self.code)
                o1 = self.orientations[i1]
                o2 = self.orientations[i2]
                if o1 == -o2:
                    possible_moves.append(ADTOp.ADTOp(2, 'D', {'arc': i}))
            if left_reg == 3:
                if self.quad(i)[2] == -self.quad(self.wrap(i + 1))[2]:
                    possible_moves.append(
                        ADTOp.ADTOp(3, 'H', {'arc': i, 'side': 'L'}))
            if right_reg == 3:
                if self.quad(i)[2] == -self.quad(self.wrap(i + 1))[2]:
                    possible_moves.append(
                        ADTOp.ADTOp(3, 'H', {'arc': i, 'side': 'R'}))
        return possible_moves

    def fineRandomMove(self):
        possible_moves = self.finePossibleMoves()
        move = random.choice(possible_moves)
        return move

    def possibleR1Up(self):
        possible_data = []
        n = self.number_crossings()
        if n > 1:
            for i in range(1, 2 * n + 1):
                for j in ['L', 'R']:
                    for k in [1, -1]:
                        possible_data.append({'arc': i, 'side': j, 'sign': k})
        else:
            for j in ['L', 'R']:
                for k in [1, -1]:
                    possible_data.append({'arc': 1, 'side': j, 'sign': k})
        return possible_data

    def possibleR1Down(self):
        possible_data = []
        n = self.number_crossings()
        for i in range(1, 2 * n + 1):
            if len(self.regions(i, 'L')) == 1 or len(self.regions(i, 'R')) == 1:
                possible_data.append({'arc': i})
        return possible_data

    def possibleR2Up(self):
        possible_data = []
        n = self.number_crossings()
        # This precludes listing R2Up moves on a single-crossing or no-crossing
        # diagram.
        if n > 1:
            for i in range(1, 2 * n + 1):
                if len(self.regions(i, 'L')) > 1:
                    left_reg = list(self.regions(i, 'L'))
                    left_reg.remove([i, self.wrap(i + 1)])
                    for j in left_reg:
                        possible_data.append(
                            {'arc': i, 'side': 'L', 'target': j})
                if len(self.regions(i, 'R')) > 1:
                    right_reg = list(self.regions(i, 'R'))
                    right_reg.remove([i, self.wrap(i + 1)])
                    for j in right_reg:
                        possible_data.append(
                            {'arc': i, 'side': 'R', 'target': j})
        return possible_data

    def possibleR2Down(self):
        possible_data = []
        n = self.number_crossings()
        for i in range(1, 2 * n + 1):
            if len(self.regions(i, 'L')) == 2 or len(self.regions(i, 'R')) == 2:
                i1 = index(i, self.code)
                i2 = index(self.wrap(i + 1), self.code)
                o1 = self.orientations[i1]
                o2 = self.orientations[i2]
                if o1 == -o2:
                    possible_data.append({'arc': i})
        return possible_data

    def possibleR3(self):
        possible_data = []
        n = self.number_crossings()
        for i in range(1, 2 * n + 1):
            if len(self.regions(i, 'L')) == 3:
                if self.quad(i)[2] != self.quad(self.wrap(i + 1)):
                    possible_data.append({'arc': i, 'side': 'L'})
            if len(self.regions(i, 'R')) == 3:
                if self.quad(i)[2] != self.quad(self.wrap(i + 1)):
                    possible_data.append({'arc': i, 'side': 'R'})
        return possible_data

    # phi_i(r) as defined in [Dowker-Thistlethwaite, page 24].
    # Says whether arc r is inside or outside the loop determined by arc i
    # and the under- or over-arc corresponding to arc i: returns -1 if
    # inside, and +1 if outside.

    def phi(self, i, r):
        r = abs(r)
        i = abs(i)
        if (i == r):
            return 1
        ar = self.jump(r)
        ai = self.jump(i)
        rm1 = self.wrap(r - 1)
        phirm1 = self.phi(i, rm1)
        if (ai > i):
            if (ar >= i and ar <= ai):
                return -phirm1
            else:
                return phirm1
        else:
            if (ar >= i and ar <= ai):
                return phirm1
            else:
                return -phirm1

    # f(i) as defined in [Dowker-Thistlethwaite, page 24].
    # Returns +1 if the other arc crosses from right to left, and -1 if it
    # crosses from left to right.

    def f(self, i):
        odd, even, sign, orient = self.quad(i)
        if (i == odd):
            return orient * sign
        if (i == even):
            return -orient * sign

    # Realisability check.
    # This is Rule 2 from [Dowker-Thistlethwaite, page 25].

    def isrealisable(self):
        n = self.number_crossings()
        for i in range(1, 2 * n + 1):
            for s in range(i + 1, 2 * n + 1):
                a_i = self.jump(i)
                a_s = self.jump(s)
                if (i < a_i) and (a_i < s) and (a_s < s):
                    phisa = self.phi(i, s) * self.phi(i, a_s)
                    if (i <= a_s) and (a_s <= a_i):
                        fi = self.f(i)
                        fs = self.f(s)
                        if phisa * fi != fs:
                            return False
                    else:
                        phisa = self.phi(i, s) * self.phi(i, a_s)
                        if phisa != 1:
                            return False
        return True

    def crossing_change(self, arc):
        n = self.number_crossings()
        arc = normalise(arc, 1, 2 * n)
        odd, even, sign, orient = self.quad(arc)
        i = (odd - 1) / 2
        self.code[i] *= -1
        self.orientations[i] *= -1
        return True

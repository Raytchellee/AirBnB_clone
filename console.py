#!/usr/bin/python3
"""Defines the HBnB console."""
import re
import cmd
from shlex import split
from models import storage
from models.user import User
from models.city import City
from models.place import Place
from models.state import State
from models.review import Review
from models.amenity import Amenity
from models.base_model import BaseModel


def parse(arg):
    """Checks input arguments"""
    braces = re.search(r"\{(.*?)\}", arg)
    brkts = re.search(r"\[(.*?)\]", arg)
    if braces is None:
        if brkts is None:
            return [idx.strip(",") for idx in split(arg)]
        else:
            subs = split(arg[:brkts.span()[0]])
            res = [idx.strip(",") for idx in subs]
            res.append(brkts.group())
            return res
    else:
        subs = split(arg[:braces.span()[0]])
        res = [idx.strip(",") for idx in subs]
        res.append(braces.group())
        return res


class HBNBCommand(cmd.Cmd):
    """Defines the HBnB cmd interpreter.
    Attributes:
        prompt: cmd prompt.
    """

    prompt = "(hbnb) "
    __classes = {
        "User",
        "City",
        "State",
        "Place",
        "Review"
        "Amenity",
        "BaseModel",
    }

    def emptyline(self):
        """Does none one empty input."""
        pass

    def default(self, arg):
        """In a case of invalid input"""
        def_dict = {
            "all": self.do_all,
            "show": self.do_show,
            "count": self.do_count,
            "update": self.do_update,
            "destroy": self.do_destroy
        }
        check = re.search(r"\.", arg)
        if check is not None:
            l_args = [arg[:check.span()[0]], arg[check.span()[1]:]]
            check = re.search(r"\((.*?)\)", l_args[1])
            if check is not None:
                command = [l_args[1][:check.span()[0]], check.group()[1:-1]]
                if command[0] in def_dict.keys():
                    call = "{} {}".format(l_args[0], command[1])
                    return def_dict[command[0]](call)
        print("*** Unknown syntax: {}".format(arg))
        return False

    def do_quit(self, arg):
        """Command to exit from program."""
        return True

    def do_EOF(self, arg):
        """End of file signal."""
        print("")
        return True

    def do_create(self, arg):
        """Usage: create <class>
        Create a new class instance and print its id.
        """
        l_arg = parse(arg)
        if len(l_arg) == 0:
            print("** class name missing **")
        elif l_arg[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            print(eval(l_arg[0])().id)
            storage.save()

    def do_show(self, arg):
        """Usage: show <class> <id> or <class>.show(<id>)
        Display the string representation of a class instance of a given id.
        """
        l_arg = parse(arg)
        objdict = storage.all()
        if len(l_arg) == 0:
            print("** class name missing **")
        elif l_arg[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(l_arg) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(l_arg[0], l_arg[1]) not in objdict:
            print("** no instance found **")
        else:
            print(objdict["{}.{}".format(l_arg[0], l_arg[1])])

    def do_destroy(self, arg):
        """Usage: destroy <class> <id> or <class>.destroy(<id>)
        Delete a class instance of a given id."""
        l_arg = parse(arg)
        objdict = storage.all()
        if len(l_arg) == 0:
            print("** class name missing **")
        elif l_arg[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(l_arg) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(l_arg[0], l_arg[1]) not in objdict.keys():
            print("** no instance found **")
        else:
            del objdict["{}.{}".format(l_arg[0], l_arg[1])]
            storage.save()

    def do_all(self, arg):
        """Usage: all or all <class> or <class>.all()
        Display string representations of all instances of a given class.
        If no class is specified, displays all instantiated objects."""
        l_arg = parse(arg)
        if len(l_arg) > 0 and l_arg[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            objl = []
            for obj in storage.all().values():
                if len(l_arg) > 0 and l_arg[0] == obj.__class__.__name__:
                    objl.append(obj.__str__())
                elif len(l_arg) == 0:
                    objl.append(obj.__str__())
            print(objl)

    def do_count(self, arg):
        """Usage: count <class> or <class>.count()
        Retrieve the number of instances of a given class."""
        l_arg = parse(arg)
        count = 0
        for obj in storage.all().values():
            if l_arg[0] == obj.__class__.__name__:
                count += 1
        print(count)

    def do_update(self, arg):
        """Usage: update <class> <id> <attribute_name> <attribute_value> or
       <class>.update(<id>, <attribute_name>, <attribute_value>) or
       <class>.update(<id>, <dictionary>)."""
        l_arg = parse(arg)
        objdict = storage.all()

        if len(l_arg) == 0:
            print("** class name missing **")
            return False
        if l_arg[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
            return False
        if len(l_arg) == 1:
            print("** instance id missing **")
            return False
        if "{}.{}".format(l_arg[0], l_arg[1]) not in objdict.keys():
            print("** no instance found **")
            return False
        if len(l_arg) == 2:
            print("** attribute name missing **")
            return False
        if len(l_arg) == 3:
            try:
                type(eval(l_arg[2])) != dict
            except NameError:
                print("** value missing **")
                return False

        if len(l_arg) == 4:
            obj = objdict["{}.{}".format(l_arg[0], l_arg[1])]
            if l_arg[2] in obj.__class__.__dict__.keys():
                valtype = type(obj.__class__.__dict__[l_arg[2]])
                obj.__dict__[l_arg[2]] = valtype(l_arg[3])
            else:
                obj.__dict__[l_arg[2]] = l_arg[3]
        elif type(eval(l_arg[2])) == dict:
            obj = objdict["{}.{}".format(l_arg[0], l_arg[1])]
            for k, v in eval(l_arg[2]).items():
                if (k in obj.__class__.__dict__.keys() and
                        type(obj.__class__.__dict__[k]) in {str, int, float}):
                    valtype = type(obj.__class__.__dict__[k])
                    obj.__dict__[k] = valtype(v)
                else:
                    obj.__dict__[k] = v
        storage.save()


if __name__ == "__main__":
    HBNBCommand().cmdloop()



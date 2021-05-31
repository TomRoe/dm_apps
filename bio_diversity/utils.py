from datetime import datetime
import decimal
import math

from pandas import read_excel
import pytz
from django.core.exceptions import ValidationError, MultipleObjectsReturned, ObjectDoesNotExist
from django.db import IntegrityError
from django.http import JsonResponse
from decimal import Decimal
from bio_diversity import models
from bio_diversity.static.calculation_constants import *


class DataParser:

    # values to explain the results of parsing
    log_data = "Loading Data Results: \n"
    success = True

    # variables counting progress
    rows_parsed = 0
    rows_entered = 0
    row_entered = False

    # the data
    cleaned_data = {}
    data = None
    data_dict = None

    # standard column headers
    year_key = "Year"
    month_key = "Month"
    day_key = "Day"

    header = 1
    converters = {year_key: str, month_key: str, day_key: str}
    sheet_name = 0
    """ The data is parsed on initializing. The process is broken into steps run sequentially in init.  Each step
     consists of two functions: a wrapper and a parser. The wrapper (eg. load_data) checks if self.success is still 
     true, catches errors from running the corresponding parser function (eg. data_loader) which should be overwritten 
     for each specific parser."""
    def __init__(self, cleaned_data, autorun=True):
        self.cleaned_data = cleaned_data
        if autorun:
            self.load_data()
            self.prep_data()
            self.iterate_rows()
            self.clean_data()
        else:
            # to run only selection of parser functions
            pass

    def load_data(self):
        try:
            self.data_reader()
            self.data_dict = self.data.to_dict('records')
        except Exception as err:
            self.log_data += "\n File format not valid: {}".format(err.__str__())
            self.success = False

    def data_reader(self):
        self.data = read_excel(self.cleaned_data["data_csv"], header=self.header, engine='openpyxl',
                               converters=self.converters, sheet_name=self.sheet_name)
        self.data = self.data.mask(self.data.eq('None')).dropna(how="all")

    def prep_data(self):
        if self.success:
            try:
                self.data_preper()
            except Exception as err:
                err_msg = common_err_parser(err)
                self.log_data += "\n Error preparing data: {}".format(err_msg)
                self.success = False

    def data_preper(self):
        pass

    def iterate_rows(self):
        for row in self.data_dict:
            if self.success:
                self.row_entered = False
                try:
                    self.row_parser(row)
                except Exception as err:
                    err_msg = common_err_parser(err)
                    self.log_data += "\nError:  {} \nError occured when parsing row: \n".format(err_msg)
                    self.log_data += str(row)
                    self.parsed_row_counter()
                    self.success = False
                self.rows_parsed += 1
                if self.row_entered:
                    self.rows_entered += 1

    def row_parser(self, row):
        pass

    def clean_data(self):
        if self.success:
            try:
                self.data_cleaner()
            except Exception as err:
                err_msg = common_err_parser(err)

                self.log_data += "Error parsing common data: \n"
                self.log_data += "\n Error: {}".format(err_msg)
                self.parsed_row_counter()
                self.success = False

            self.parsed_row_counter()

    def data_cleaner(self):
        pass

    def parsed_row_counter(self):
        self.log_data += "\n\n\n {} of {} rows parsed \n {} of {} rows entered into database.  " \
                         "\n".format(self.rows_parsed, len(self.data_dict), self.rows_entered, len(self.data_dict))

    def team_parser(self, init_str, row, role_id=None, loc_id=None):
        if nan_to_none(init_str):
            perc_list, inits_not_found = team_list_splitter(init_str)
            for perc_id in perc_list:
                self.row_entered += add_team_member(perc_id, self.cleaned_data["evnt_id"], role_id=role_id, loc_id=loc_id)
            for inits in inits_not_found:
                self.log_data += "No valid personnel with initials ({}) on row: \n{}\n".format(inits, row)


def bio_diverisity_authorized(user):
    # return user.is_user and user.groups.filter(name='bio_diversity_user').exists()
    return user.groups.filter(name='bio_diversity_user').exists() or bio_diverisity_admin(user)


def bio_diverisity_admin(user):
    # return user.is_authenticated and user.groups.filter(name='bio_diversity_admin').exists()
    return user.groups.filter(name='bio_diversity_admin').exists()


def get_comment_keywords_dict():
    my_dict = {}
    for obj in models.CommentKeywords.objects.all():
        my_dict[obj.keyword] = obj.adsc_id
    return my_dict


def get_help_text_dict(model=None, title=''):
    my_dict = {}
    if not model:
        for obj in models.HelpText.objects.all():
            my_dict[obj.field_name] = str(obj)
    else:
        # If a model is supplied get the fields specific to that model
        for obj in models.HelpText.objects.filter(model=str(model.__name__)):
            my_dict[obj.field_name] = str(obj)

    return my_dict


def team_list_splitter(team_str, valid_only=True):
    team_str_list = team_str.split(",")
    team_str_list = [indv_str.strip() for indv_str in team_str_list]
    all_perc_qs = models.PersonnelCode.objects.filter(perc_valid=valid_only)
    found_list = []
    not_found_list = []
    for inits in team_str_list:
        perc_qs = all_perc_qs.filter(initials__iexact=inits)
        try:
            found_list.append(perc_qs.get())
        except (MultipleObjectsReturned, ObjectDoesNotExist):
            not_found_list.append(inits)
    return found_list, not_found_list


def year_coll_splitter(full_str):
    coll = full_str.lstrip(' 0123456789')
    year = int(full_str[:len(full_str) - len(coll)])
    return year, coll.strip()


def val_unit_splitter(full_str):
    unit_str = full_str.lstrip(' 0123456789.')
    val = float(full_str[:len(full_str) - len(unit_str)])
    return val, unit_str.strip()


def daily_dev(degree_day):
    dev = 100 / math.exp(DEVELOPMENT_ALPHA * math.exp(DEVELOPMENT_BETA * degree_day))
    return dev


def condition_factor(len_cm, weight_g):
    return 100 * float(weight_g) / (float(len_cm) ** 3)


def parse_concentration(concentration_str):
    if "%" in concentration_str:
        return Decimal(float(concentration_str.rstrip("%"))/100)
    elif ":" in concentration_str:
        concentration_str = concentration_str.replace(" ", "")
        concentration_str = concentration_str.replace("1:", "", 1)
        return Decimal(1.0/float(concentration_str))
    else:
        return None


def get_cont_evnt(contx_tuple):
    # input should be in the form (contx, bool/null)
    contx = contx_tuple[0]
    in_out_dict = {None: "", False: "Origin", True: "Destination"}
    output_list = [contx.evnt_id.evntc_id.__str__(), contx.evnt_id.start_date, in_out_dict[contx_tuple[1]]]
    for cont in [contx.tank_id, contx.cup_id, contx.tray_id, contx.trof_id, contx.draw_id, contx.heat_id]:
        if cont:
            output_list.append("{}".format(cont.__str__()))
            break
    return output_list


def get_cont_from_anix(anix, cont_key):
    if cont_key == "tank":
        return anix.contx_id.tank_id
    elif cont_key == "tray":
        return anix.contx_id.tray_id
    elif cont_key == "trof":
        return anix.contx_id.trof_id
    elif cont_key == "cup":
        return anix.contx_id.cup_id
    elif cont_key == "heat":
        return anix.contx_id.heat_id
    elif cont_key == "draw":
        return anix.contx_id.draw_id
    elif cont_key is None:
        all_conts = [anix.contx_id.tank_id, anix.contx_id.tray_id, anix.contx_id.trof_id, anix.contx_id.cup_id, anix.contx_id.heat_id, anix.contx_id.draw_id]
        return [cont for cont in all_conts if cont][0]
    else:
        return None


def get_cont_from_dot(dot_string, cleaned_data, start_date):
    dot_string = str(dot_string)
    cup = get_cup_from_dot(dot_string, cleaned_data, start_date)
    if cup:
        return cup
    else:
        draw = get_draw_from_dot(dot_string, cleaned_data)
        if draw:
            return draw
        else:
            tank_qs = models.Tank.objects.filter(name__icontains=dot_string)
            if len(tank_qs) == 1:
                return tank_qs.get()
            else:
                return None


def get_cup_from_dot(dot_string, cleaned_data, start_date):
    cont_list = dot_string.split(".")
    if len(cont_list) == 3:
        heat, draw, cup = cont_list
    else:
        return None
    cup_qs = models.Cup.objects.filter(name=cup, draw_id__name=draw, draw_id__heat_id__name=heat, draw_id__heat_id__facic_id=cleaned_data["facic_id"], end_date__isnull=True)
    if cup_qs.exists():
        return cup_qs.get()
    else:
        cup_obj = models.Cup(name=cup,
                             start_date=start_date,
                             draw_id=models.Drawer.objects.filter(name=draw, heat_id__name=heat, heat_id__facic_id=cleaned_data["facic_id"]).get(),
                             description_en="Autogenerated by parser",
                             created_by=cleaned_data["created_by"],
                             created_date=cleaned_data["created_date"],
                             )
        try:
            cup_obj.clean()
            cup_obj.save()
        except (ValidationError, IntegrityError):
            return None
        return cup_obj


def get_draw_from_dot(dot_string, cleaned_data):
    cont_list = dot_string.split(".")
    if len(cont_list) == 2:
        heat, draw = cont_list
    else:
        return None
    draw_qs = models.Drawer.objects.filter(name=draw, heat_id__name=heat, heat_id__facic_id=cleaned_data["facic_id"])
    if draw_qs.exists():
        return draw_qs.get()
    else:
        return


def get_grp(stock_str, grp_year, coll_str, cont=None, at_date=datetime.now().replace(tzinfo=pytz.UTC), prog_grp=None, prog_str=None, fail_on_not_found=False):

    if nan_to_none(prog_str):
        prog_grp = models.AniDetSubjCode.objects.filter(name__iexact=prog_str).get()

    if cont:
        indv_list, grp_list =cont.fish_in_cont(at_date, select_fields=["grp_id__coll_id", "grp_id__stok_id"])
        grp_list = [grp for grp in grp_list if grp.stok_id.name == stock_str and coll_str in grp.coll_id.name
                    and grp.grp_year == grp_year]

    else:
        grp_qs = models.Group.objects.filter(stok_id__name=stock_str,
                                             coll_id__name__icontains=coll_str,
                                             grp_year=grp_year)

        grp_list = [grp for grp in grp_qs]

    final_grp_list = grp_list.copy()
    if prog_grp:
        final_grp_list = []
        for grp in grp_list:
            if prog_grp in grp.prog_group():
                final_grp_list.append(grp)

    if len(final_grp_list) == 0 and fail_on_not_found:
        if cont:
            raise Exception("\nGroup {}-{}-{} in container {} and program group {} not uniquely found in"
                            " db\n".format(stock_str, grp_year, coll_str, cont.name, prog_str))
        else:
            raise Exception("\nGroup {}-{}-{} with program group {} not uniquely found in"
                            " db\n".format(stock_str, grp_year, coll_str, prog_str))
    return final_grp_list


def get_relc_from_point(shapely_geom):
    relc_qs = models.ReleaseSiteCode.objects.all()
    for relc in relc_qs:
        # need to add infinitesimal buffer to deal with rounding issue
        if relc.bbox:
            if relc.bbox.buffer(1e-14).intersects(shapely_geom):
                return relc
    return None


def get_row_date(row):
    try:
        row_datetime = datetime.strptime(row["Year"] + "-" + row["Month"] + "-" + row["Day"],
                                         "%Y-%b-%d").replace(tzinfo=pytz.UTC)
    except Exception as err:
        raise Exception("\nFailed to parse date from row, make sure column headers are : \"Year\", \"Month\", \"Day\" "
                        "and the format used is: 1999-Jan-1 \n \n {}".format(err))

    return row_datetime


def comment_parser(comment_str, anix_indv, det_date):
    data_entered = False
    com_key_dict = get_comment_keywords_dict()
    parser_list = com_key_dict.keys()
    mortality = False
    parsed = False
    for term in parser_list:
        if term.lower() in comment_str.lower():
            parsed = True
            adsc = com_key_dict[term]
            if adsc.name == "Mortality":
                mortality = True
            indvd_parsed = models.IndividualDet(anix_id_id=anix_indv.pk,
                                                anidc_id=adsc.anidc_id,
                                                adsc_id=adsc,
                                                qual_id=models.QualCode.objects.filter(name="Good").get(),
                                                detail_date=det_date,
                                                comments=comment_str,
                                                created_by=anix_indv.created_by,
                                                created_date=anix_indv.created_date,
                                                )
            try:
                indvd_parsed.clean()
                indvd_parsed.save()
                data_entered = True
            except (ValidationError, IntegrityError):
                pass
    if mortality:
        parsed = True
        if anix_indv.indv_id.indv_valid:
            data_entered = True
        anix_indv.indv_id.indv_valid = False
        anix_indv.indv_id.save()
    return parsed, data_entered


def create_movement_evnt(origin, destination, cleaned_data, movement_date, indv_pk=None, grp_pk=None, return_end_contx=False):
    row_entered = False
    end_contx = False
    origin_conts = []
    movement_date = naive_to_aware(movement_date)
    new_cleaned_data = cleaned_data.copy()
    if origin == destination:
        row_entered = False
        return row_entered
    if "evnt_id" in cleaned_data.keys():
        if cleaned_data["evnt_id"]:
            # link containers to parent event
            if not origin:
                # move indvidual or group to destination and clean up previous contx's
                if grp_pk:
                    grp = models.Group.objects.filter(pk=grp_pk).get()
                    origin_conts = grp.current_cont(movement_date)
            else:
                row_entered += enter_contx(origin, cleaned_data, None)

            row_entered += enter_contx(destination, cleaned_data, None)

    if destination:
        movement_evnt = models.Event(evntc_id=models.EventCode.objects.filter(name="Movement").get(),
                                     facic_id=cleaned_data["evnt_id"].facic_id,
                                     perc_id=cleaned_data["evnt_id"].perc_id,
                                     prog_id=cleaned_data["evnt_id"].prog_id,
                                     start_datetime=movement_date,
                                     end_datetime=movement_date,
                                     created_by=new_cleaned_data["created_by"],
                                     created_date=new_cleaned_data["created_date"],
                                     )
        try:
            movement_evnt.clean()
            movement_evnt.save()
            row_entered = True
        except (ValidationError, IntegrityError):
            movement_evnt = models.Event.objects.filter(evntc_id=movement_evnt.evntc_id,
                                                        facic_id=movement_evnt.facic_id,
                                                        prog_id=movement_evnt.prog_id,
                                                        start_datetime=movement_evnt.start_datetime,
                                                        end_datetime=movement_evnt.end_datetime,
                                                        ).get()

        new_cleaned_data["evnt_id"] = movement_evnt
        if indv_pk:
            row_entered += enter_anix(new_cleaned_data, indv_pk=indv_pk, return_sucess=True)
        if grp_pk:
            row_entered += enter_anix(new_cleaned_data, grp_pk=grp_pk, return_sucess=True)
        if origin:
            row_entered += enter_contx(origin, new_cleaned_data, False, indv_pk=indv_pk, grp_pk=grp_pk)
        elif origin_conts:
            for cont in origin_conts:
                if not cont == destination:
                    row_entered += enter_contx(cont, new_cleaned_data, False, indv_pk=indv_pk, grp_pk=grp_pk)
        end_contx, data_entered = enter_contx(destination, new_cleaned_data, True, indv_pk=indv_pk, grp_pk=grp_pk,
                                              return_contx=True)
        row_entered += data_entered

    if return_end_contx:
        return end_contx
    else:
        return row_entered


def create_new_evnt(cleaned_data, evntc_name, evnt_date):
    new_cleaned_data = cleaned_data.copy()
    new_evnt = models.Event(evntc_id=models.EventCode.objects.filter(name=evntc_name).get(),
                            facic_id=cleaned_data["evnt_id"].facic_id,
                            perc_id=cleaned_data["evnt_id"].perc_id,
                            prog_id=cleaned_data["evnt_id"].prog_id,
                            start_datetime=evnt_date,
                            end_datetime=evnt_date,
                            created_by=cleaned_data["created_by"],
                            created_date=cleaned_data["created_date"],
                            )
    try:
        new_evnt.clean()
        new_evnt.save()
    except (ValidationError, IntegrityError):
        new_evnt = models.Event.objects.filter(evntc_id=new_evnt.evntc_id,
                                               facic_id=new_evnt.facic_id,
                                               prog_id=new_evnt.prog_id,
                                               start_datetime=new_evnt.start_datetime,
                                               end_datetime=new_evnt.end_datetime,
                                               ).get()

    new_cleaned_data["evnt_id"] = new_evnt
    return new_cleaned_data


def create_feed_evnt(cleaned_data):
    new_evnt = models.Event(evntc_id=models.EventCode.objects.filter(name="Feeding").get(),
                            facic_id=cleaned_data["facic_id"],
                            perc_id=cleaned_data["perc_id"],
                            prog_id=cleaned_data["prog_id"],
                            start_datetime=cleaned_data["feed_date"],
                            end_datetime=cleaned_data["feed_date"],
                            created_by=cleaned_data["created_by"],
                            created_date=cleaned_data["created_date"],
                            )
    try:
        new_evnt.clean()
        new_evnt.save()
    except (ValidationError, IntegrityError):
        new_evnt = models.Event.objects.filter(evntc_id=new_evnt.evntc_id,
                                               facic_id=new_evnt.facic_id,
                                               prog_id=new_evnt.prog_id,
                                               start_datetime=new_evnt.start_datetime,
                                               end_datetime=new_evnt.end_datetime,
                                               ).get()

    return new_evnt


def create_egg_movement_evnt(tray, cup, cleaned_data, movement_date, grp_pk, return_cup_contx=False):
    # moves eggs from trof-tray to heat.draw.cup, only use the final group as this splits groups
    # cup argument can also be a drawer object
    row_entered = False
    new_cleaned_data = cleaned_data.copy()

    movement_evnt = models.Event(evntc_id=models.EventCode.objects.filter(name="Movement").get(),
                                 facic_id=cleaned_data["evnt_id"].facic_id,
                                 perc_id=cleaned_data["evnt_id"].perc_id,
                                 prog_id=cleaned_data["evnt_id"].prog_id,
                                 start_datetime=movement_date,
                                 end_datetime=movement_date,
                                 created_by=new_cleaned_data["created_by"],
                                 created_date=new_cleaned_data["created_date"],
                                 )
    try:
        movement_evnt.clean()
        movement_evnt.save()
        row_entered = True
    except (ValidationError, IntegrityError):
        movement_evnt = models.Event.objects.filter(evntc_id=movement_evnt.evntc_id,
                                                    facic_id=movement_evnt.facic_id,
                                                    prog_id=movement_evnt.prog_id,
                                                    start_datetime=movement_evnt.start_datetime,
                                                    end_datetime=movement_evnt.end_datetime,
                                                    ).get()

    new_cleaned_data["evnt_id"] = movement_evnt
    if grp_pk:
        enter_anix(new_cleaned_data, grp_pk=grp_pk)
    tray_contx, data_entered = enter_contx(tray, new_cleaned_data, False, None, grp_pk=grp_pk, return_contx=True)
    if tray_contx:
        row_entered = True
    cup_contx, data_entered = enter_contx(cup, new_cleaned_data, True, None, grp_pk=grp_pk, return_contx=True)
    if cup_contx:
        row_entered = True
    if return_cup_contx:
        return cup_contx
    else:
        return row_entered


def create_picks_evnt(cleaned_data, tray, grp_pk, pick_cnt, pick_datetime, cnt_code):
    row_entered = False
    new_cleaned_data = cleaned_data.copy()

    pick_evnt = models.Event(evntc_id=models.EventCode.objects.filter(name="Picking").get(),
                             facic_id=cleaned_data["evnt_id"].facic_id,
                             perc_id=cleaned_data["evnt_id"].perc_id,
                             prog_id=cleaned_data["evnt_id"].prog_id,
                             start_datetime=pick_datetime,
                             end_datetime=pick_datetime,
                             created_by=new_cleaned_data["created_by"],
                             created_date=new_cleaned_data["created_date"],
                             )
    try:
        pick_evnt.clean()
        pick_evnt.save()
        row_entered = True
    except (ValidationError, IntegrityError):
        pick_evnt = models.Event.objects.filter(evntc_id=pick_evnt.evntc_id,
                                                facic_id=pick_evnt.facic_id,
                                                prog_id=pick_evnt.prog_id,
                                                start_datetime=pick_evnt.start_datetime,
                                                end_datetime=pick_evnt.end_datetime,
                                                ).get()

    new_cleaned_data["evnt_id"] = pick_evnt
    if grp_pk:
        enter_anix(new_cleaned_data, grp_pk=grp_pk)
    contx, data_entered = enter_contx(tray, new_cleaned_data, None, grp_pk=grp_pk, return_contx=True)
    if contx:
        row_entered = True
        enter_cnt(cleaned_data, pick_cnt, contx_pk=contx.pk, cnt_code=cnt_code)

    return row_entered


def add_team_member(perc_id, evnt_id, loc_id=None, role_id=None, return_team=False):
    row_entered = False
    team = models.TeamXRef(perc_id=perc_id,
                           evnt_id=evnt_id,
                           loc_id=loc_id,
                           role_id=role_id,
                           created_by=evnt_id.created_by,
                           created_date=evnt_id.created_date,
                           )
    try:
        team.clean()
        team.save()
        row_entered = True
    except (ValidationError, IntegrityError):
        team = models.TeamXRef.objects.filter(perc_id=team.perc_id, evnt_id=team.evnt_id, loc_id=team.loc_id,
                                              role_id=team.role_id).get()
    if return_team:
        return team, row_entered

    return row_entered


def create_tray(trof, tray_name, start_date, cleaned_data, save=True):
    tray = models.Tray(trof_id=trof,
                       name=tray_name,
                       description_en="Auto generated tray",
                       start_date=start_date,
                       created_by=cleaned_data["created_by"],
                       created_date=cleaned_data["created_date"],
                       )
    try:
        if save:
            tray.clean()
            tray.save()
    except (ValidationError, IntegrityError):
        tray = models.Tray.objects.filter(trof_id=tray.trof_id, name=tray.name, start_date=tray.start_date).get()
    return tray


def enter_anix(cleaned_data, indv_pk=None, contx_pk=None, loc_pk=None, pair_pk=None, grp_pk=None, indvt_pk=None, team_pk=None, final_flag=None, return_sucess=False, return_anix=False):
    row_entered = False
    if any([indv_pk, contx_pk, loc_pk, pair_pk, grp_pk, indvt_pk, team_pk]):
        anix = models.AniDetailXref(evnt_id_id=cleaned_data["evnt_id"].pk,
                                    indv_id_id=indv_pk,
                                    contx_id_id=contx_pk,
                                    loc_id_id=loc_pk,
                                    pair_id_id=pair_pk,
                                    grp_id_id=grp_pk,
                                    indvt_id_id=indvt_pk,
                                    team_id_id=team_pk,
                                    final_contx_flag=final_flag,
                                    created_by=cleaned_data["created_by"],
                                    created_date=cleaned_data["created_date"],
                                    )
        try:
            anix.clean()
            anix.save()
            row_entered = True
        except ValidationError:
            anix = models.AniDetailXref.objects.filter(evnt_id=anix.evnt_id,
                                                       indv_id=anix.indv_id,
                                                       contx_id=anix.contx_id,
                                                       loc_id=anix.loc_id,
                                                       pair_id=anix.pair_id,
                                                       grp_id=anix.grp_id,
                                                       team_id=anix.team_id,
                                                       indvt_id=anix.indvt_id,
                                                       ).get()
        if return_anix:
            return anix
        elif return_sucess:
            return row_entered
        else:
            return anix, row_entered


def enter_anix_contx(tank, cleaned_data):
    if tank:
        contx = models.ContainerXRef(evnt_id=cleaned_data["evnt_id"],
                                     tank_id=tank,
                                     created_by=cleaned_data["created_by"],
                                     created_date=cleaned_data["created_date"],
                                     )
        try:
            contx.clean()
            contx.save()
            return contx
        except ValidationError:
            contx = models.ContainerXRef.objects.filter(evnt_id=contx.evnt_id,
                                                        tank=contx.tank_id,
                                                        ).get()

        anix_contx = enter_anix(cleaned_data, contx_pk=contx.pk, return_anix=True)
        return anix_contx


def enter_cnt(cleaned_data, cnt_value, contx_pk=None, loc_pk=None, cnt_code="Fish in Container", est=False):
    cnt = False
    entered = False
    if cnt_value is None:
        return False, False
    if not math.isnan(cnt_value):
        cnt = models.Count(loc_id_id=loc_pk,
                           contx_id_id=contx_pk,
                           spec_id=models.SpeciesCode.objects.filter(name__iexact="Salmon").get(),
                           cntc_id=models.CountCode.objects.filter(name__iexact=cnt_code).get(),
                           cnt=int(cnt_value),
                           est=est,
                           created_by=cleaned_data["created_by"],
                           created_date=cleaned_data["created_date"],
                           )
        try:
            cnt.clean()
            cnt.save()
            entered = True
        except ValidationError:
            cnt = models.Count.objects.filter(loc_id=cnt.loc_id, contx_id=cnt.contx_id, cntc_id=cnt.cntc_id).get()
            if cnt_code == "Mortality":
                cnt.cnt += 1
                cnt.save()
    return cnt, entered


def enter_cnt_det(cleaned_data, cnt, det_val, det_code, det_subj_code=None, qual="Good"):
    row_entered = False
    # checks for truthness of det_val and if its a nan. Fails for None and nan (nan == nan is false), passes for values
    det_val = nan_to_none(det_val)

    if det_val:
        if type(det_val) != str:
            det_val = round(decimal.Decimal(det_val), 5)
        if not det_subj_code:
            cntd = models.CountDet(cnt_id=cnt,
                                   anidc_id=models.AnimalDetCode.objects.filter(name__iexact=det_code).get(),
                                   det_val=det_val,
                                   qual_id=models.QualCode.objects.filter(name=qual).get(),
                                   created_by=cleaned_data["created_by"],
                                   created_date=cleaned_data["created_date"],
                                   )
        else:
            cntd = models.CountDet(cnt_id=cnt,
                                   anidc_id=models.AnimalDetCode.objects.filter(name__iexact=det_code).get(),
                                   adsc_id=models.AniDetSubjCode.objects.filter(name__iexact=det_subj_code).get(),
                                   det_val=det_val,
                                   qual_id=models.QualCode.objects.filter(name=qual).get(),
                                   created_by=cleaned_data["created_by"],
                                   created_date=cleaned_data["created_date"],
                                   )
        try:
            cntd.clean()
            cntd.save()
            row_entered = True
        except (ValidationError, IntegrityError):
            row_entered = False

        # update count total if needed:
        if det_code == "Program Group":
            new_cnt = sum([float(cnt) for cnt in models.CountDet.objects.filter(cnt_id=cnt, anidc_id__name__iexact=det_code).values_list('det_val', flat=True)])
            if new_cnt > cnt.cnt:
                cnt.cnt = int(new_cnt)
                cnt.save()
                row_entered = True

    return row_entered


def enter_env(env_value, env_date, cleaned_data, envc_id, envsc_id=None, loc_id=None, contx=None, inst_id=None,
              env_start=None, avg=False, save=True, qual_id=False):
    row_entered = False
    if not nan_to_none(env_value):
        return False
    if env_start:
        env_datetime = naive_to_aware(env_date, env_start)
    else:
        env_datetime = naive_to_aware(env_date)

    if not qual_id:
        qual_id = models.QualCode.objects.filter(name="Good").get()

    if envsc_id:
        env = models.EnvCondition(contx_id=contx,
                                  loc_id=loc_id,
                                  envc_id=envc_id,
                                  envsc_id=envsc_id,
                                  inst_id=inst_id,
                                  env_val=str(env_value),
                                  env_avg=avg,
                                  start_datetime=env_datetime,
                                  qual_id=qual_id,
                                  created_by=cleaned_data["created_by"],
                                  created_date=cleaned_data["created_date"],
                                  )
    else:
        env = models.EnvCondition(contx_id=contx,
                                  loc_id=loc_id,
                                  envc_id=envc_id,
                                  inst_id=inst_id,
                                  env_val=str(env_value),
                                  env_avg=avg,
                                  start_datetime=env_datetime,
                                  qual_id=qual_id,
                                  created_by=cleaned_data["created_by"],
                                  created_date=cleaned_data["created_date"],
                                  )
    if save:
        try:
            env.clean()
            env.save()
            row_entered = True
        except (ValidationError, IntegrityError):
            pass
        return row_entered
    else:
        try:
            env.clean()
            return env
        except (ValidationError, IntegrityError):
            return None


def enter_feed(cleaned_data, contx_id, feedc_id, feedm_id, amt, comments=None, freq=None, lot_num=None):
    row_entered = False
    feed = models.Feeding(contx_id=contx_id,
                          feedm_id=feedm_id,
                          feedc_id=feedc_id,
                          lot_num=lot_num,
                          amt=amt,
                          unit_id=models.UnitCode.objects.filter(name="Feed Size").get(),
                          comments=comments,
                          freq=freq,
                          created_by=cleaned_data["created_by"],
                          created_date=cleaned_data["created_date"],
                          )
    try:
        feed.clean()
        feed.save()
        row_entered = True
    except (ValidationError, IntegrityError):
        pass
    return row_entered


def enter_grpd(anix_pk, cleaned_data, det_date, det_value, anidc_pk, anidc_str=None, adsc_str=None, frm_grp_id=None, comments=None):
    row_entered = False
    if isinstance(det_value, float):
        if math.isnan(det_value):
            return False
    if anidc_str:
        anidc_pk = models.AnimalDetCode.objects.filter(name=anidc_str).get().pk

    if adsc_str:
        grpd = models.GroupDet(anix_id_id=anix_pk,
                               anidc_id_id=anidc_pk,
                               adsc_id=models.AniDetSubjCode.objects.filter(name=adsc_str).get(),
                               frm_grp_id=frm_grp_id,
                               det_val=det_value,
                               detail_date=det_date,
                               qual_id=models.QualCode.objects.filter(name="Good").get(),
                               comments=comments,
                               created_by=cleaned_data["created_by"],
                               created_date=cleaned_data["created_date"],
                               )
    else:
        grpd = models.GroupDet(anix_id_id=anix_pk,
                               anidc_id_id=anidc_pk,
                               frm_grp_id=frm_grp_id,
                               det_val=det_value,
                               detail_date=det_date,
                               qual_id=models.QualCode.objects.filter(name="Good").get(),
                               created_by=cleaned_data["created_by"],
                               created_date=cleaned_data["created_date"],
                               )
    try:
        grpd.clean()
        grpd.save()
        row_entered = True
    except (ValidationError, IntegrityError):
        pass
    return row_entered


def enter_indvd(anix_pk, cleaned_data, det_date, det_value, anidc_pk, adsc_str=None, comments=None):
    row_entered = False
    if isinstance(det_value, float):
        if math.isnan(det_value):
            return False
    if adsc_str:
        indvd = models.IndividualDet(anix_id_id=anix_pk,
                                     anidc_id_id=anidc_pk,
                                     adsc_id=models.AniDetSubjCode.objects.filter(name=adsc_str).get(),
                                     det_val=det_value,
                                     detail_date=det_date,
                                     qual_id=models.QualCode.objects.filter(name="Good").get(),
                                     comments=comments,
                                     created_by=cleaned_data["created_by"],
                                     created_date=cleaned_data["created_date"],
                                     )
    else:
        indvd = models.IndividualDet(anix_id_id=anix_pk,
                                     anidc_id_id=anidc_pk,
                                     det_val=det_value,
                                     detail_date=det_date,
                                     qual_id=models.QualCode.objects.filter(name="Good").get(),
                                     created_by=cleaned_data["created_by"],
                                     created_date=cleaned_data["created_date"],
                                     )
    try:
        indvd.clean()
        indvd.save()
        row_entered = True
    except (ValidationError, IntegrityError):
        pass
    return row_entered


def enter_locd(loc_pk, cleaned_data, det_date, det_value, locdc_pk, ldsc_str=None, comments=None):
    row_entered = False
    if isinstance(det_value, float):
        if math.isnan(det_value):
            return False
    if ldsc_str:
        locd = models.LocationDet(loc_id_id=loc_pk,
                                  locdc_id_id=locdc_pk,
                                  ldsc_id=models.LocDetSubjCode.objects.filter(name=ldsc_str).get(),
                                  det_val=det_value,
                                  detail_date=det_date,
                                  qual_id=models.QualCode.objects.filter(name="Good").get(),
                                  comments=comments,
                                  created_by=cleaned_data["created_by"],
                                  created_date=cleaned_data["created_date"],
                                  )
    else:
        locd = models.LocationDet(loc_id_id=loc_pk,
                                  locdc_id_id=locdc_pk,
                                  det_val=det_value,
                                  detail_date=det_date,
                                  qual_id=models.QualCode.objects.filter(name="Good").get(),
                                  created_by=cleaned_data["created_by"],
                                  created_date=cleaned_data["created_date"],
                                  )
    try:
        locd.clean()
        locd.save()
        row_entered = True
    except (ValidationError, IntegrityError):
        pass
    return row_entered


def enter_mortality(indv, cleaned_data, mort_date):
    data_entered = False
    mortality_evnt = models.Event(evntc_id=models.EventCode.objects.filter(name="Mortality").get(),
                                  facic_id=cleaned_data["evnt_id"].facic_id,
                                  prog_id=cleaned_data["evnt_id"].prog_id,
                                  perc_id=cleaned_data["evnt_id"].perc_id,
                                  start_datetime=mort_date,
                                  end_datetime=mort_date,
                                  created_by=cleaned_data["created_by"],
                                  created_date=cleaned_data["created_date"],
                                  )
    try:
        mortality_evnt.clean()
        mortality_evnt.save()
        data_entered = True
    except (ValidationError, IntegrityError):
        mortality_evnt = models.Event.objects.filter(evntc_id=mortality_evnt.evntc_id,
                                                     facic_id=mortality_evnt.facic_id,
                                                     prog_id=mortality_evnt.prog_id,
                                                     start_datetime=mortality_evnt.start_datetime,
                                                     end_datetime=mortality_evnt.end_datetime,
                                                     ).get()
    new_cleaned_data = cleaned_data.copy()
    new_cleaned_data["evnt_id"] = mortality_evnt
    anix, anix_entered = enter_anix(new_cleaned_data, indv_pk=indv.pk)
    data_entered += anix_entered
    indv.indv_valid = False
    indv.save()
    return mortality_evnt, anix, data_entered


def enter_samp(cleaned_data, samp_num, spec_pk, sampc_pk, anix_pk=None, loc_pk=None):
    samp_entered = False
    samp = models.Sample(anix_id_id=anix_pk,
                         loc_id_id=loc_pk,
                         spec_id_id=spec_pk,
                         samp_num=samp_num,
                         sampc_id_id=sampc_pk,
                         created_by=cleaned_data["created_by"],
                         created_date=cleaned_data["created_date"],
                         )
    try:
        samp.clean()
        samp.save()
        samp_entered = True
    except (ValidationError, IntegrityError):
        samp = models.Sample.objects.filter(anix_id=samp.anix_id,
                                            loc_id=samp.loc_id,
                                            spec_id=samp.spec_id,
                                            samp_num=samp.samp_num,
                                            sampc_id=samp.sampc_id,
                                            ).get()

    return samp, samp_entered


def enter_sampd(samp_pk, cleaned_data, det_date, det_value, anidc_pk, anidc_str=None, adsc_str=None, comments=None):
    row_entered = False
    if not nan_to_none(det_value):
        return False
    if anidc_str:
        anidc_pk = models.AnimalDetCode.objects.filter(name=anidc_str).get().pk
    if adsc_str:
        sampd = models.SampleDet(samp_id_id=samp_pk,
                                 anidc_id_id=anidc_pk,
                                 adsc_id=models.AniDetSubjCode.objects.filter(name=adsc_str).get(),
                                 det_val=det_value,
                                 detail_date=det_date,
                                 qual_id=models.QualCode.objects.filter(name="Good").get(),
                                 comments=comments,
                                 created_by=cleaned_data["created_by"],
                                 created_date=cleaned_data["created_date"],
                                 )
    else:
        sampd = models.SampleDet(samp_id_id=samp_pk,
                                 anidc_id_id=anidc_pk,
                                 det_val=det_value,
                                 detail_date=det_date,
                                 qual_id=models.QualCode.objects.filter(name="Good").get(),
                                 created_by=cleaned_data["created_by"],
                                 created_date=cleaned_data["created_date"],
                                 )
    try:
        sampd.clean()
        sampd.save()
        row_entered = True
    except (ValidationError, IntegrityError):
        pass
    return row_entered


def enter_spwnd(pair_pk, cleaned_data, det_value, spwndc_pk, spwnsc_str, qual_code="Good", comments=None):
    row_entered = False
    if isinstance(det_value, float):
        if math.isnan(det_value):
            return False
    if spwnsc_str:
        spwnd = models.SpawnDet(pair_id_id=pair_pk,
                                spwndc_id_id=spwndc_pk,
                                spwnsc_id=models.SpawnDetSubjCode.objects.filter(name=spwnsc_str).get(),
                                det_val=det_value,
                                qual_id=models.QualCode.objects.filter(name=qual_code).get(),
                                comments=comments,
                                created_by=cleaned_data["created_by"],
                                created_date=cleaned_data["created_date"],
                                )
    else:
        spwnd = models.SpawnDet(pair_id_id=pair_pk,
                                spwndc_id_id=spwndc_pk,
                                det_val=det_value,
                                qual_id=models.QualCode.objects.filter(name=qual_code).get(),
                                created_by=cleaned_data["created_by"],
                                created_date=cleaned_data["created_date"],
                                )
    try:
        spwnd.clean()
        spwnd.save()
        row_entered = True
    except ValidationError:
        pass
    return row_entered


def enter_contx(cont, cleaned_data, final_flag=None, indv_pk=None, grp_pk=None, team_pk=None, return_contx=False):
    cont_type = type(cont)
    if cont_type == models.Tank:
        return enter_tank_contx(cont.name, cleaned_data, final_flag, indv_pk, grp_pk, team_pk, return_contx)
    elif cont_type == models.Trough:
        return enter_trof_contx(cont.name, cleaned_data, final_flag, indv_pk, grp_pk, team_pk, return_contx)
    elif cont_type == models.Tray:
        return enter_tray_contx(cont, cleaned_data, final_flag, indv_pk, grp_pk, team_pk, return_contx)
    elif cont_type == models.Cup:
        return enter_cup_contx(cont, cleaned_data, final_flag, indv_pk, grp_pk, team_pk, return_contx)
    elif cont_type == models.Drawer:
        return enter_draw_contx(cont, cleaned_data, final_flag, indv_pk, grp_pk, team_pk, return_contx)
    elif cont_type == models.HeathUnit:
        return enter_heat_contx(cont, cleaned_data, final_flag, indv_pk, grp_pk, team_pk, return_contx)


def enter_tank_contx(tank_name, cleaned_data, final_flag=None, indv_pk=None, grp_pk=None, team_pk=None, return_contx=False):
    row_entered = False
    if not tank_name == "nan":
        contx = models.ContainerXRef(evnt_id_id=cleaned_data["evnt_id"].pk,
                                     tank_id=models.Tank.objects.filter(name=tank_name, facic_id=cleaned_data["facic_id"]).get(),
                                     team_id_id=team_pk,
                                     created_by=cleaned_data["created_by"],
                                     created_date=cleaned_data["created_date"],
                                     )
        try:
            contx.clean()
            contx.save()
            row_entered = True
        except ValidationError:
            contx = models.ContainerXRef.objects.filter(evnt_id=contx.evnt_id,
                                                        tank_id=contx.tank_id,
                                                        team_id=contx.team_id).get()
        if indv_pk or grp_pk:
            row_entered += enter_anix(cleaned_data, indv_pk=indv_pk, grp_pk=grp_pk, contx_pk=contx.pk, final_flag=final_flag, return_sucess=True)
        if return_contx:
            return contx, row_entered
        else:
            return row_entered
    else:
        return False


def enter_trof_contx(trof_name, cleaned_data, final_flag=None, indv_pk=None, grp_pk=None, team_pk=None, return_contx=False):
    row_entered = False
    if not trof_name == "nan":
        contx = models.ContainerXRef(evnt_id_id=cleaned_data["evnt_id"].pk,
                                     trof_id=models.Trough.objects.filter(name=trof_name, facic_id=cleaned_data["facic_id"]).get(),
                                     team_id_id=team_pk,
                                     created_by=cleaned_data["created_by"],
                                     created_date=cleaned_data["created_date"],
                                     )
        try:
            contx.clean()
            contx.save()
            row_entered = True
        except ValidationError:
            contx = models.ContainerXRef.objects.filter(evnt_id=contx.evnt_id,
                                                        trof_id=contx.trof_id,
                                                        team_id=contx.team_id).get()
        if indv_pk or grp_pk:
            row_entered += enter_anix(cleaned_data, indv_pk=indv_pk, grp_pk=grp_pk, contx_pk=contx.pk, final_flag=final_flag, return_sucess=True)
        if return_contx:
            return contx, row_entered
        else:
            return row_entered
    else:
        return False


def enter_tray_contx(tray, cleaned_data, final_flag=None, indv_pk=None, grp_pk=None, team_pk=None, return_contx=False):
    row_entered = False
    if not tray == "nan":
        contx = models.ContainerXRef(evnt_id_id=cleaned_data["evnt_id"].pk,
                                     tray_id=tray,
                                     team_id_id=team_pk,
                                     created_by=cleaned_data["created_by"],
                                     created_date=cleaned_data["created_date"],
                                     )
        try:
            contx.clean()
            contx.save()
            row_entered = True
        except ValidationError:
            contx = models.ContainerXRef.objects.filter(evnt_id=contx.evnt_id,
                                                        tray_id=contx.tray_id,
                                                        team_id=contx.team_id).get()
        if indv_pk or grp_pk:
            row_entered += enter_anix(cleaned_data, indv_pk=indv_pk, grp_pk=grp_pk, contx_pk=contx.pk,
                                      final_flag=final_flag, return_sucess=True)
        if return_contx:
            return contx, row_entered
        else:
            return row_entered
    else:
        return False


def enter_cup_contx(cup, cleaned_data, final_flag=None, indv_pk=None, grp_pk=None, team_pk=None, return_contx=False):
    row_entered = False
    if not cup == "nan":
        contx = models.ContainerXRef(evnt_id_id=cleaned_data["evnt_id"].pk,
                                     cup_id=cup,
                                     team_id_id=team_pk,
                                     created_by=cleaned_data["created_by"],
                                     created_date=cleaned_data["created_date"],
                                     )
        try:
            contx.clean()
            contx.save()
            row_entered = True
        except ValidationError:
            contx = models.ContainerXRef.objects.filter(evnt_id=contx.evnt_id,
                                                        cup_id=contx.cup_id,
                                                        team_id=contx.team_id).get()

        draw_contx = models.ContainerXRef(evnt_id_id=cleaned_data["evnt_id"].pk,
                                          draw_id=cup.draw_id,
                                          created_by=cleaned_data["created_by"],
                                          created_date=cleaned_data["created_date"],
                                          )
        try:
            draw_contx.clean()
            draw_contx.save()
            row_entered = True
        except ValidationError:
            pass

        heat_contx = models.ContainerXRef(evnt_id_id=cleaned_data["evnt_id"].pk,
                                          heat_id=cup.draw_id.heat_id,
                                          created_by=cleaned_data["created_by"],
                                          created_date=cleaned_data["created_date"],
                                          )
        try:
            heat_contx.clean()
            heat_contx.save()
            row_entered = True
        except ValidationError:
            pass

        if indv_pk or grp_pk:
            row_entered += enter_anix(cleaned_data, indv_pk=indv_pk, grp_pk=grp_pk, contx_pk=contx.pk,
                                      final_flag=final_flag, return_sucess=True)
        if return_contx:
            return contx, row_entered
        else:
            return row_entered
    else:
        return False


def enter_draw_contx(draw, cleaned_data, final_flag=None, indv_pk=None, grp_pk=None, team_pk=None, return_contx=False):
    row_entered = False
    if draw:
        contx = models.ContainerXRef(evnt_id_id=cleaned_data["evnt_id"].pk,
                                     draw_id=draw,
                                     team_id_id=team_pk,
                                     created_by=cleaned_data["created_by"],
                                     created_date=cleaned_data["created_date"],
                                     )
        try:
            contx.clean()
            contx.save()
            row_entered = True
        except ValidationError:
            contx = models.ContainerXRef.objects.filter(evnt_id=contx.evnt_id,
                                                        draw_id=contx.draw_id,
                                                        team_id=contx.team_id).get()

        heat_contx = models.ContainerXRef(evnt_id_id=cleaned_data["evnt_id"].pk,
                                          heat_id=draw.heat_id,
                                          created_by=cleaned_data["created_by"],
                                          created_date=cleaned_data["created_date"],
                                          )
        try:
            heat_contx.clean()
            heat_contx.save()
            row_entered = True
        except ValidationError:
            pass

        if indv_pk or grp_pk:
            row_entered += enter_anix(cleaned_data, indv_pk=indv_pk, grp_pk=grp_pk, contx_pk=contx.pk,
                                      final_flag=final_flag, return_sucess=True)
        if return_contx:
            return contx, row_entered
        else:
            return row_entered
    else:
        return False


def enter_heat_contx(heat, cleaned_data, final_flag=None, indv_pk=None, grp_pk=None, team_pk=None, return_contx=False):
    row_entered = False
    if heat:
        contx = models.ContainerXRef(evnt_id_id=cleaned_data["evnt_id"].pk,
                                     heat_id=heat,
                                     team_id_id=team_pk,
                                     created_by=cleaned_data["created_by"],
                                     created_date=cleaned_data["created_date"],
                                     )
        try:
            contx.clean()
            contx.save()
            row_entered = True
        except ValidationError:
            contx = models.ContainerXRef.objects.filter(evnt_id=contx.evnt_id,
                                                        heat_id=contx.heat_id,
                                                        team_id=contx.team_id).get()

        if indv_pk or grp_pk:
            row_entered += enter_anix(cleaned_data, indv_pk=indv_pk, grp_pk=grp_pk, contx_pk=contx.pk,
                                      final_flag=final_flag, return_sucess=True)
        if return_contx:
            return contx, row_entered
        else:
            return row_entered
    else:
        return False


def ajax_get_fields(request):
    model_name = request.GET.get('model', None)

    # use the model name passed from the web page to find the model in the apps models file
    model = models.__dict__[model_name]

    # use the retrieved model and get the doc string which is a string in the format
    # SomeModelName(id, field1, field2, field3)
    # remove the trailing parentheses, split the string up based on ', ', then drop the first element
    # which is the model name and the id.
    match = str(model.__dict__['__doc__']).replace(")", "").split(", ")[1:]
    fields = list()
    for f in match:
        label = "---"
        attr = getattr(model, f).field
        if hasattr(attr, 'verbose_name'):
            label = attr.verbose_name

        fields.append([f, label])

    data = {
        'fields': fields
    }

    return JsonResponse(data)


def naive_to_aware(naive_date, naive_time=datetime.min.time()):
    # adds null time and timezone to dates
    return datetime.combine(naive_date, naive_time).replace(tzinfo=pytz.UTC)


def nan_to_none(test_item):
    if type(test_item) == float:
        if math.isnan(test_item):
            return None
    elif test_item == "nan":
        return None

    return test_item


def y_n_to_bool(test_item):
    if type(test_item) == float:
        if math.isnan(test_item):
            return False
        elif test_item:
            return True
    elif test_item.upper() == "Y":
        return True
    else:
        return False


def round_no_nan(data, precision):
    # data can be nan, decimal, float, etc.
    if data is None:
        return None
    elif math.isnan(data):
        return None
    else:
        return round(decimal.Decimal(data), precision)


def common_err_parser(err):
    err_msg = err.__str__()
    if type(err) == KeyError:
        err_msg = "Column with header \"{}\" not found in worksheet".format(err)

    if issubclass(type(err), ObjectDoesNotExist):
        err_msg = "Could not find a {} object from worksheet in database.".format(err.__str__().split(" ")[0])

    return err_msg


def get_cont_from_tag(cont_tag, cont_id):
    cont = None
    if cont_tag == "cup":
        cont = models.Cup.objects.filter(pk=cont_id).get()
    elif cont_tag == "draw":
        cont = models.Drawer.objects.filter(pk=cont_id).get()
    elif cont_tag == "heat":
        cont = models.HeathUnit.objects.filter(pk=cont_id).get()
    elif cont_tag == "tank":
        cont = models.Tank.objects.filter(pk=cont_id).get()
    elif cont_tag == "tray":
        cont = models.Tray.objects.filter(pk=cont_id).get()
    elif cont_tag == "trof":
        cont = models.Trough.objects.filter(pk=cont_id).get()
    return cont

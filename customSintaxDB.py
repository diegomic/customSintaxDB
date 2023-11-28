#!/usr/local/bin/python3.6
# encoding: utf-8
"""
 -- 

@author:     Diego Micheletti

@copyright:  2022 FEM. All rights reserved.

@license:    


@deffield    updated: Updated
"""


import argparse
from textwrap import dedent
from Bio import SeqIO
from Bio import Entrez
import sys


def get_opt():
    """
    Command line options.
    """
    try:
        # Setup argument parser
        parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
        parser.add_argument('-l', '--list', type=str, help='File with the list of entry to search')
        parser.add_argument('-o', '--output', type=str, help='Output File basename')
        parser.add_argument('-g', '--gene', type=str, help='gene to search in entrez')
        parser.add_argument('-f', '--field', type=str, default='gene', 
                            help='NCBI field in which the gene is searched. To search in all field set to None or none')
        entrez = parser.add_argument_group("Entrez - NCBI's E-utilities")
        entrez.add_argument('--email', type=str, default=None,
                            help=dedent('''\
                                Email to use for make queries through to NCBI's E-utilities, if email is empty a 
                                warning is raised by the Entrez module. To make use of NCBI's 
                                E-utilities, NCBI requires you to specify your email address with each request.'''))
        entrez.add_argument('--api_key', type=str, default=None,
                            help=dedent('''\
                                API key to use for make queries through to NCBI's E-utilities, if empty a 
                                warning is raised by the Entrez module. Personal API key from NCBI. If not set, only 
                                3 queries per second are allowed. 10 queries per seconds otherwise with a valid API key.
                                '''))
        entrez.add_argument('--max_tries', type=int, default=3,
                            help='Configures how many times failed requests will be automatically retried on error.')

        entrez.add_argument('--sleep_between_tries', type=int, default=15,
                            help='The delay, in seconds, before retrying a request on error.')

        if len(sys.argv) == 1:
            parser.print_help()
            sys.exit(1)
        else:
            return parser.parse_args()

    except Exception as e:
        print('\nUnexpected error. Read the help\nErrorType:', e)
        # parser.print_help()
        return 2


def get_taxa(mysp, flog):
    try:
        handle_search = Entrez.esearch(db="taxonomy", retmax=10, term=f"{mysp}", idtype="acc")
        record = Entrez.read(handle_search)
        handle_search.close()
        # print(record)
        handle = Entrez.efetch(db="taxonomy", id=record["IdList"], rettype="xml")
        # print(handle)
        taxrec = Entrez.read(handle)
    except RuntimeError as e:
        print(mysp, e, sep='\t', file=flog)
        return
    except:
        print(mysp, 'except', sep='\t', file=flog)
        return
    if len(taxrec) == 1:
        tax = taxrec[0]
        taxa = ','.join([f"{rank['Rank'][0]}:{rank['ScientificName']}" for rank in tax['LineageEx']
                         if not rank['Rank'] in ('clade', 'no rank', 'superkingdom')])
        taxa += f",s:{tax['ScientificName']}"
        return taxa
    elif len(taxrec) == 0:
        print(mysp, 'not in taxonomy', sep='\t', file=flog)
        return
    else:
        print(mysp, 'multiple taxa records', sep='\t', file=flog)
        return


def main():
    args = get_opt()
    print(args)
    if args.email:
        Entrez.email = args.email
    if args.api_key:
        Entrez.api_key = args.api_key
    if args.max_tries:
        Entrez.max_tries = args.max_tries
    if args.sleep_between_tries:
        Entrez.sleep_between_tries = args.sleep_between_tries

    with open(f"{args.output}.fasta", 'w') as fout, open(f'{args.output}.log.txt', 'w') as flog:
        orgno,recno = 0, 0
        for i, mysp in enumerate(open(args.list)):
            orgno += 1
            # if i % 10 == 0:
            mysp = mysp.strip()
            #print(mysp)
            taxa = get_taxa(mysp, flog)
            if not taxa:
                print(mysp, 'noTaxa', sep='\t', file=flog)
                continue
            field = '' if not args.field else f"[{args.field}]"
            #qprint(f"({args.gene} {field}) AND ({mysp} [orgn])",)
            handle_search = Entrez.esearch(db="nucleotide", retmax=1000,
                                           term=f'({args.gene}) AND ("{mysp}" [orgn])',
                                           idtype="acc")
            record = Entrez.read(handle_search)
            handle_search.close()
            print(record)
            if int(record['Count']) == 0:
                # print(mysp)
                print(mysp, 'recordCount==0', sep='\t', file=flog)
                continue
            handle = Entrez.efetch(db="nucleotide", id=record["IdList"], rettype="gb", retmax=1000)
            gbrecs = SeqIO.parse(handle, 'genbank')
            # print(mysp, record, taxa)
            for rec in gbrecs:
                try:
                    if len(rec.seq) > 0:
                        #print(mysp, rec, taxa)
                        print(f">{rec.id};tax={taxa}\n{rec.seq}", file=fout)
                        recno += 1
                    else:
                        print(mysp, 'seqLen==0', sep='\t', file=flog)
                except Exception as e:
                    print(mysp, e, rec.id, rec.description, sep='\t', file=flog)
            handle.close()
        print(f"# Number of species to search:  {orgno}", file=flog)
        print(f"# Number of records found:  {recno}", file=flog)


if __name__ == "__main__":
    main()
